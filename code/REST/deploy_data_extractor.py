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
    
    
def run(api_token):
  try: 
    # api parameters
    city_ids = ['5747882', '5809844', '5799841', '5816449', '5812944', '5786882']
    city_batch = ",".join(city_ids)
    cities = ['Redmond, WA, USA','Seattle, WA, USA', 'Kirkland, WA, USA', 'Woodinville, WA, USA', 'Tacoma, WA, USA', 'Bellevue, WA, USA']
    
    response = requests.get("http://api.openweathermap.org/data/2.5/group?id=" + city_batch + "&appid=" + api_token)
    
    return json.loads(response.content)

  except Exception as e: 
    return str(e)
    
""" 
 
 
exec(weather_data_extractor)
 
with open("weather_data_extractor.py", "w") as file:
    file.write(weather_data_extractor)


# Create a dependencies file
from azureml.core.conda_dependencies import CondaDependencies 

myenv = CondaDependencies.create(conda_packages=['numpy'], pip_packages=['requests', 'datetime', 'time'])

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

data = requests.post(service.scoring_uri, manager.weather_api_token, headers={'Content-Type':'application/json'})
data.content
