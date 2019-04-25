import azureml.core
from azureml.core import Workspace
from azureml.core.webservice import Webservice
from azureml.core.authentication import ServicePrincipalAuthentication
import logging, os
import requests, json
from azure.datalake.store import core, lib


from app_manager import AppManager
manager = AppManager()

## Connect to our Azure Machine Learning Workspace
auth_obj = ServicePrincipalAuthentication(manager.azure_tenant_id, manager.client_id, manager.client_secret)
ws = Workspace.get(name=manager.aml_workspace_name, auth=auth_obj, subscription_id=manager.azure_subscription_id, resource_group=manager.aml_resource_group )



def get_aml_service_data(service_name):
    webservice = ws.webservices[service_name]


    data = requests.post(webservice.scoring_uri, manager.weather_api_token, headers={'Content-Type': 'application/json'})
    return data.content

def connect_adls(manager):
        """
        Creates a connection to Azure Data Lake Store
        """
        adls = None
        try:
            token = lib.auth(tenant_id=manager.azure_tenant_id, 
                client_id=manager.client_id, 
                client_secret=manager.client_secret, 
                resource='https://datalake.azure.net/')

            adls = core.AzureDLFileSystem(token, store_name=manager.adls_name)

        except Exception as ex:
            print("Unable to connect to Azure Data Lake! Error: %s" % (str(ex)))

        return adls

def write_json_file(manager, adls, output_path, data):
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