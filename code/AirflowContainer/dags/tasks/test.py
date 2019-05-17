
import azureml.core
from azureml.core import Workspace
from azureml.core.webservice import Webservice
from azureml.core.authentication import ServicePrincipalAuthentication
import requests
from tasks.app_manager import AppManager



service_name = 'weatherdataextractor'
manager = AppManager()

## Connect to our Azure Machine Learning Workspace
auth_obj = ServicePrincipalAuthentication(manager.azure_tenant_id, manager.client_id, manager.client_secret)
ws = Workspace.get(name=manager.aml_workspace_name, auth=auth_obj, subscription_id=manager.azure_subscription_id, resource_group=manager.aml_resource_group )

webservice = ws.webservices[service_name]

data = requests.post(webservice.scoring_uri, manager.weather_api_token, headers={'Content-Type': 'application/json'})



