import azureml.core
from azureml.core import Workspace, Run
from azureml.core.model import Model
from azureml.core.authentication import ServicePrincipalAuthentication
import logging, os

from app_manager import AppManager
manager = AppManager()


## Connect to our Azure Machine Learning Workspace
auth_obj = ServicePrincipalAuthentication(manager.azure_tenant_id, manager.client_id, manager.client_secret)
ws = Workspace.get(name=manager.aml_workspace_name, auth=auth_obj, subscription_id=manager.azure_subscription_id, resource_group=manager.aml_resource_group )


deploy_folder = os.getcwd()


weather_data_extractor = """
import json, requests
import numpy as np
import os, sys
import datetime, time

def init():    
  return None
    
    
def run(manager):
  try: 
    adls_connect_obj = manager.connect_adls()

    # api parameters
    city_ids = ['5747882', '5809844', '5799841', '5816449', '5812944', '5786882']
    city_batch = ",".join(city_ids)
    cities = ['Redmond, WA, USA','Seattle, WA, USA', 'Kirkland, WA, USA', 'Woodinville, WA, USA', 'Tacoma, WA, USA', 'Bellevue, WA, USA']
    
    response = requests.get("http://api.openweathermap.org/data/2.5/group?id=" + city_batch + "&appid=" + manager.weather_api_token)
    
    output_datetime = datetime.datetime.utcnow()
    data_output_path = "raw/weather_data/{}/{}/{}/{}/{}/weather_data.json".format(output_datetime.year, output_datetime.month, output_datetime.day, output_datetime.hour, output_datetime.minute)

    # write json file to adls
    manager.write_json_file(adls_connect_obj, data_output_path, response.content.decode('utf8'))

    return "200: Success"

  except Exception as e: 
    return str(e)
    
""" 
 
 
exec(weather_data_extractor)
 
with open("weather_data_extractor.py", "w") as file:
    file.write(weather_data_extractor)


# Create a dependencies file
from azureml.core.conda_dependencies import CondaDependencies 

myenv = CondaDependencies.create(conda_packages=['numpy', 'json', 'requests', 'datetime', 'time'])

with open("weather_env_file.yml","w") as f:
    f.write(myenv.serialize_to_string())


# ACI Configuration
from azureml.core.webservice import AciWebservice, Webservice

myaci_config = AciWebservice.deploy_configuration(cpu_cores=1, 
             memory_gb=1, 
             tags={"data": "weather data extraction"}, 
             description='Extracts weather data from source and lands it in ADLS.')


# deploy to aci
from azureml.core.webservice import Webservice
from azureml.core.image import ContainerImage

# configure the image
image_config = ContainerImage.image_configuration(execution_script="weather_data_extractor.py", 
                                                  runtime="python", 
                                                  conda_file="weather_env_file.yml", 
                                                  description = "Weather Data Extractor",
                                                  tags = {"data": "Weather"}
                                                )

service = Webservice.deploy_from_model(workspace=ws,
                                       name='weatherdataextractor',
                                       deployment_config=myaci_config,
                                       models=[],
                                       image_config=image_config)

service.wait_for_deployment(show_output=True)

# print the uri of the web service
print(service.scoring_uri)



#### test the web service
import requests
import json

# we don't want to send nan to our webservice. Replace with 0. 
test_data = pd.read_csv("data/titanic_test.csv").fillna(value=0).values
# send a random row from the test set to score
random_index = np.random.randint(0, len(test_data)-1)
## we want to use double quotes in our json
input_data = "{\"data\": [" + str(list(test_data[random_index])).replace("\'", "\"") + "]}"

headers = {'Content-Type':'application/json'}

resp = requests.post(service.scoring_uri, input_data, headers=headers)


print("POST to url", service.scoring_uri)
print("label:", test_data[random_index])
print("prediction:", resp.text)
