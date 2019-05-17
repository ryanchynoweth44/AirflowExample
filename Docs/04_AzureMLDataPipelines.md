# Creating a Data Pipeline with Apache Airflow and Azure Machine Learning Services

Deploying data pipelines in containers is an easy way to manage dependencies, orchestrate workflows, and schedule your jobs. When deploying data pipelines as containers I will write my Python code using the Azure Machine Learning service (Azure ML Service) since it allows for easy configuration and security of web services. For the sake of this demo we will be borrowing code from a recent [blog post](https://ryansdataspot.com/2019/03/14/data-analytics-data-engineering-and-containers/) of mine where I walk developers through the process of deploying Python code as containers in Azure. 

Please note that the use of Azure ML Service is for ease of use. The Azure ML Service essentially wraps a developers Python code as a docker container and exposes a REST endpoint using the popular python library Flask. Therefore, we could write all the authentication and security code ourselves but it is just easier to use this product.   

To provide a quick overview for this section of our Apache Airflow demo we will:
1. Write extraction code from an a free weather data source
1. Wrap our extractor up using Azure Machine Learning Services
1. Develop a generalized library to execute web services
1. Develop a DAG to execute our data extractor every 10 minutes. 
1. Deploy code and resources to Azure

## Creating Azure Resources

1. First we will want to create an Azure Machine Learning Service Workspace (Azure ML Workspace). Navigate to [Azure](https://portal.azure.com) to create the resource. Please use the Azure ML [documentation](https://docs.microsoft.com/en-us/azure/machine-learning/service/setup-create-workspace) for more detailed instructions. Your Azure 


1. Next we will also want to create and configure an Azure Data Lake Store. We will use the Azure Data Lake Store as a landing spot for all our raw data sources. [Create an Azure Data Lake Store.](https://docs.microsoft.com/en-us/azure/data-lake-store/data-lake-store-get-started-portal#create-a-data-lake-storage-gen1-account) by following the linked instructions.  

1. Once your data lake is created you will need to [create a service principle.](https://docs.microsoft.com/en-us/azure/active-directory/develop/howto-create-service-principal-portal) A service principle is esstentially a secure way to handle service accounts in Azure.   

1. Now that you have created a service principle you will need to give it access to your Azure Data Lake Store by following these [instructions.](https://docs.microsoft.com/en-us/azure/data-lake-store/data-lake-store-secure-data#filepermissions) 
    - Check out access control rules [here.](https://docs.microsoft.com/en-us/azure/data-lake-store/data-lake-store-access-control)  


## Data Extractor

We will be borrowing the [code](https://github.com/ryanchynoweth44/DataPipelinesUsingContainers/blob/master/code/application/extract_data.py) from a previous demo I created where we extract weather data from various locations every 10 minutes, however, the code will need a few edits in order to get it ready for Azure ML. 

1. In this walkthrough we will be using a separate conda environment to develop our data extractor. To set up a new conda environment and install the appropriate library please run the following in an anaconda command prompt. 
    ```
    conda create -n amlenv python=3.6

    conda activate amlenv

    pip install azureml-sdk
    pip install azure
    ```

1. In our working directory (`code`) create a folder named `REST`. This will be the location we write our data extractor in. 

1. First we will create an application manager class to help store secrets and manage the actions for our data extractor. Create `app_manager.py` and paste the following code. Please note that if you would like to run this locally then you will need to pip install azure in your airflow environment.  
    ```python
    import sys, os
    from azure.datalake.store import core, lib
    import json
    import configparser


    class AppManager(object):
        """
        This class is a helper class for the data extractor. It supplies function to extract data and write it to adls. 
        """

        def __init__(self, config_file="app_config.conf", env="DEV"):
            self.weather_api_token = None
            self.azure_tenant_id = None
            self.azure_subscription_id = None
            self.adls_client_id = None
            self.adls_client_secret = None
            self.adls_name = None
            self.aml_workspace_name = None
            self.aml_resource_group = None
            self.aml_location = None
            self.set_config(config_file)

        def set_config(self, config_file,  env="DEV"):
            """
            Sets configuration variables for the application
            :param config_file: the path to the configuration file
            :param env: the environment string to parse in config file
            :return None
            """
            config = configparser.RawConfigParser(allow_no_value=True)
            
            config.read(filenames = [config_file])
                
            ### Setting values here ###
            self.weather_api_token = config.get(env, "WEATHER_API_TOKEN")
            self.azure_tenant_id = config.get(env, "AZURE_TENANT_ID")
            self.azure_subscription_id = config.get(env, "AZURE_SUBSCRIPTION_ID")
            self.client_id = config.get(env, "CLIENT_ID")
            self.client_secret = config.get(env, "CLIENT_SECRET")
            self.adls_name = config.get(env, "ADLS_NAME")
            self.aml_workspace_name = config.get(env, "AML_WORKSPACE_NAME")
            self.aml_resource_group = config.get(env, "AML_RESOURCE_GROUP")
            self.aml_location = config.get(env, "AML_LOCATION")

        def connect_adls(self):
            """
            Creates a connection to Azure Data Lake Store
            """
            adls = None
            try:
                token = lib.auth(tenant_id=self.azure_tenant_id, 
                    client_id=self.client_id, 
                    client_secret=self.client_secret, 
                    resource='https://datalake.azure.net/')

                adls = core.AzureDLFileSystem(token, store_name=self.adls_name)

            except Exception as ex:
                print("Unable to connect to Azure Data Lake! Error: %s" % (str(ex)))

            return adls

        def write_json_file(self, adls, output_path, data):
            """
            Writes json files to Azure Data Lake Store
            :param adls: Instance of ADLS
            :param output_path: the file path to write to in ADLS
            :param data: data to write in file. Data must be decoded using .decode('utf8').
            :return string saying if it successfully wrote data
            """
            try:
                with adls.open(output_path, 'ab') as outfile:
                    outfile.write(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')).encode())
                return "Wrote to ADLS"
            except IOError as iex:
                print("ADL Write to File: Error while writing data to file on ADL " + str(iex))
                return "Unable to write to ADLS"
    ```

1. We will also need to create a configuration file. My gitignore file ensures that my config file is not inside my repository, however, you will want to create a config file called `app_config.conf`. The config file has the following format: 
    ```
    [WeatherConfig]
    WEATHER_API_TOKEN = <Weather API Token>
    AZURE_TENANT_ID = <Tenant Id>
    AZURE_SUBSCRIPTION_ID = <Subscription Id>
    CLIENT_ID = <Service Principle/Client Id>
    CLIENT_SECRET = <Client Secret>
    ADLS_NAME = <Data Lake Name>
    AML_WORKSPACE_NAME = <Azure ML Workspace>
    AML_RESOURCE_GROUP = <Azure ML RG>
    AML_LOCATION = <Azure ML Resource Region>
    ```
    Note that it is not always best to store these secrets in a configuration file, because techinically anyone with read access to the container we will create could access these secrets.  

1. Next we will create a `deploy_data_extractor.py` file and import the following libraries. This is simply a python script that we use to connect to our Azure ML workspace, create a Docker Container, and deploy that container to Azure Container Instance. 
    ```python
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
    # api parameters
    city_ids = ['5747882', '5809844', '5799841', '5816449', '5812944', '5786882']
    city_batch = ",".join(city_ids)
    cities = ['Redmond, WA, USA','Seattle, WA, USA', 'Kirkland, WA, USA', 'Woodinville, WA, USA', 'Tacoma, WA, USA', 'Bellevue, WA, USA']
    
    response = requests.get("http://api.openweathermap.org/data/2.5/group?id=" + city_batch + "&appid=" + api_token)
    
    return json.loads(response.content)    
    """ 
    
    exec(weather_data_extractor)
    # write extractor to file
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

    # build the image
    image_config = ContainerImage.image_configuration(execution_script="weather_data_extractor.py", 
                                                    runtime="python", 
                                                    conda_file="weather_env_file.yml", 
                                                    description = "Weather Data Extractor",
                                                    tags = {"data": "Weather"}
                                                    )

    # deploy as docker container
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

    ```
    We have now deployed a data extractor web service using the Azure Machine Learning service. Please note that while this may seem to create more overhead, it does make it easier to manage when data transforms or extractions are more complex. 


## Scheduling, Monitoring, and Managing our Data Extractor

Now that we have developed and deployed a data extraction pipeline in Azure, we need to schedule the execution and ensure that it is running successfully. To do so we will use a few generic Python tasks to create and schedule an Airflow DAG. 

1. First, in our `tasks` folder we will create a python script called `aml_tasks.py`. This script ideally contains tasks that are required to call web services. Currently we require only a single task that can call any Azure Machine Learning web service. 
    ```python
    import azureml.core
    from azureml.core import Workspace
    from azureml.core.webservice import Webservice
    from azureml.core.authentication import ServicePrincipalAuthentication
    import requests
    from tasks.app_manager import AppManager


    def get_aml_service_data(**kwargs):
        service_name = kwargs['service_name']
        output_path = kwargs['output_path']
        manager = AppManager()
        ## Connect to our Azure Machine Learning Workspace
        auth_obj = ServicePrincipalAuthentication(manager.azure_tenant_id, manager.client_id, manager.client_secret)
        ws = Workspace.get(name=manager.aml_workspace_name, auth=auth_obj, subscription_id=manager.azure_subscription_id, resource_group=manager.aml_resource_group )

        webservice = ws.webservices[service_name]

        data = requests.post(webservice.scoring_uri, manager.weather_api_token, headers={'Content-Type': 'application/json'})

        adls = manager.connect_adls()
        manager.write_json_file(adls, output_path, data.content.decode('utf8'))
    ```


1. Next we will want to create and schedule our DAG so that we actually execute our recently deployed data pipeline. 
    ```python
    import datetime as dt
    import os, sys
    from airflow import DAG
    from airflow.operators.python_operator import PythonOperator
    from airflow.operators.bash_operator import BashOperator

    # import our task library
    from tasks import aml_tasks

    current_dt = dt.datetime.utcnow()
    start_date = dt.datetime(current_dt.year, current_dt.month, current_dt.day)

    output_weather_data_path = "raw/weather_data/{}/{}/{}/{}/{}/weather_data.json".format(current_dt.year, current_dt.month, current_dt.day, current_dt.hour, current_dt.minute)

    ## configure settings that are shared by all tasks in our DAG
    default_args = {
        'owner': 'Ryan Chynoweth',
        'start_date': start_date,
        'retries': 1,
        'retry_delay': dt.timedelta(minutes=2),
    }


    ## Run the execution every 30 minutes
    dag = DAG('weather_data_extraction', default_args=default_args, schedule_interval='*/30 * * * *')

    ## create the task using the python function
    ## Note here that we pass parameters using the 'op_kwargs' parameter
    get_weather_data = PythonOperator(task_id='get_weather_data', provide_context=True, python_callable=aml_tasks.get_aml_service_data, op_kwargs={'service_name': 'weatherdataextractor', 'output_path': output_weather_data_path}, dag=dag, catchup=False )
    ```

1. In addition to the two scripts above, we will want to copy and paste the `app_config.conf` and `app_manager.py` files into the `tasks` folder. This may seem redundent but keep in mind that the data extractor is decoupled and deployed separate from our Airflow DAGs, and web service data pipelines may be in a completely separate repository.  


## Running Airflow Locally

Now that you have developed your data extractor and DAG to execute, lets run Airflow locally to see it in action. Please note that you will need to run Airflow from the [Ubuntu Virtual Machine](./01_CreateUbuntuVM.md) we created in the first step of this walk through. 

1. Open two command prompts, and activate our airflow environment on both prompts. 
    ```
    conda activate airflow
    ```

1. Next we want to set our Airflow Home Directory to the same directory on both prompts. I would recommend using the parent directory of your `dags` folder. In my case it is the `code\AirflowContainer` folder.  
    ```
    export AIRFLOW_HOME="<YOUR PATH>
    ```

1. Initialize your Airflow SQLite database by running the following in one of your prompts.
    ```
    airflow initdb
    ```
1. In the `airflow.cfg` make the following changes: 
    ```
    load_examples = False
    catch_up_by_default = False
    dags_are_paused_at_creation = False 
    ``` 

1. Start your Airflow Webserver in one of your prompts. Then navigate to localhost:8080 using a web browser. 
    ```
    airflow webserver --port 8080
    ```
1. Start the Airflow Scheduler in the other prompt. This will automatically pick up and run any new dags in your `dags` folder. 
    ```
    airflow scheduler
    ```

Now that airflow is running you should be able to see new weather data files in your Azure Data Lake Store!

