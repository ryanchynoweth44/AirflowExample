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