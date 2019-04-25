## Creating a Simple Data Pipeline with Apache Airflow

Deploying data pipelines in containers is an easy way to manage dependencies, orchestrate workflows, and schedule your jobs. When deploying data pipelines as containers I will write my Python code using the Azure Machine Learning service (Azure ML Service) since it allows for easy configuration and security of web services. For the sake of this demo we will be borrowing code from a recent [blog post](https://ryansdataspot.com/2019/03/14/data-analytics-data-engineering-and-containers/) of mine where I walk developers through the process of deploying Python code as containers in Azure. 

Please note that the use of Azure ML Service is for ease of use. The Azure ML Service essentially wraps a developers Python code as a docker container and exposes a REST endpoint using the popular python library Flask. Therefore, we could write all the authentication and security code ourselves but it is just easier to use this product.   

To provide a quick overview for this section of our Apache Airflow demo we will:
1. Write extraction code from an a free weather data source
1. Wrap our extractor up using Azure Machine Learning Services
1. Develop a generalized library to execute web services
1. Develop a DAG to execute our data extractor every 10 minutes. 
1. Deploy code and resources to Azure

### Creating Azure Resources

1. First we will want to create an Azure Machine Learning Service Workspace (Azure ML Workspace). Navigate to [Azure](https://portal.azure.com) to create the resource. Please use the Azure ML [documentation](https://docs.microsoft.com/en-us/azure/machine-learning/service/setup-create-workspace) for more detailed instructions. Your Azure 


1. Next we will also want to create and configure an Azure Data Lake Store. We will use the Azure Data Lake Store as a landing spot for all our raw data sources. [Create an Azure Data Lake Store.](https://docs.microsoft.com/en-us/azure/data-lake-store/data-lake-store-get-started-portal#create-a-data-lake-storage-gen1-account) by following the linked instructions.  

1. Once your data lake is created you will need to [create a service principle.](https://docs.microsoft.com/en-us/azure/active-directory/develop/howto-create-service-principal-portal) A service principle is esstentially a secure way to handle service accounts in Azure.   

1. Now that you have created a service principle you will need to give it access to your Azure Data Lake Store by following these [instructions.](https://docs.microsoft.com/en-us/azure/data-lake-store/data-lake-store-secure-data#filepermissions) 
    - Check out access control rules [here.](https://docs.microsoft.com/en-us/azure/data-lake-store/data-lake-store-access-control)  


### Data Extractor

We will be borrowing the [code](https://github.com/ryanchynoweth44/DataPipelinesUsingContainers/blob/master/code/application/extract_data.py) from a previous demo I created where we extract weather data from various locations every 10 minutes, however, the code will need a few edits in order to get it ready for Azure ML. 

1. In this walkthrough we will be using a separate conda environment to develop our data extractor. To set up a new conda environment and install the appropriate library please run the following in an anaconda command prompt. 
    ```
    conda create -n amlenv python=3.5

    conda activate amlenv

    pip install azureml-sdk
    pip install azure
    ```

1. In our working directory (`code`) create a folder named `REST`. This will be the location we write our data extractor in. 

1. First we will create an application manager class to help store secrets and manage the actions for our data extractor. Create `app_manager.py` and paste the following code. Please note that if you would like to run this locally then you will need to pip install azure in your airflow environment.  
    ```python
    
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

1. Next we will create a `deploy_data_extractor.py` file and import the following libraries.
    ```python

    ```

1. We need to connect to our Azure Machine Learning Workspace. We can do so with the following code: 
    ```python


    ```


