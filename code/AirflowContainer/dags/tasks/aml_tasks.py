import azureml.core
from azureml.core import Workspace
from azureml.core.webservice import Webservice
from azureml.core.authentication import ServicePrincipalAuthentication
import requests
from tasks.app_manager import AppManager


def get_aml_service_data(**kwargs):
    # try :
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
    #     return "200: Success"
    # except Exception as e :
    #     return str(e)

