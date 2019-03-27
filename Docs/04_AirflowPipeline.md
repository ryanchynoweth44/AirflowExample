## Creating a Simple Data Pipeline with Apache Airflow

Deploying data pipelines in containers is an easy way to manage dependencies, orchestrate workflows, and schedule your jobs. When deploying data pipelines as containers I will write my process as a RESTful web service that executes when triggered. To create the web service I will use the popular Python library Flask in union with Azure resources for security and deployment. For the sake of this demo we will be borrowing code from a recent [blog post](https://ryansdataspot.com/2019/03/14/data-analytics-data-engineering-and-containers/) of mine where I walk developers through the process of deploying Python code as containers in Azure. 

To provide a quick overview for this section of our Apache Airflow demo we will:
1. Deploy resources in Azure
1. Write extraction code from an a free weather data source
1. Write a DAG to execute code on a schedule



### Deploying Azure Resources

Writing secure code is extremely important, and is not as easy as it should be. Running data pipelines in containers is tricky because anyone who has read access to the container registry essentailly has access to the source code, including any secrets that could be found in configuration files. In attempt to be more secure we will deploy an Azure Key Vault to managed all of our secrets, the only issue is then that we do need to store service credentials in our configuration file, but this does avoid storing all our secrets in the container, therefore, secure enough for this demo. If you want to take it an extra step, I would recommend using [managed service identities with azure container instances](https://docs.microsoft.com/en-us/azure/container-instances/container-instances-managed-identity). 


1. Navigate the [Azure Portal](https://portal.azure.com) and search for Key Vault.

1. Create Key Vault

1. Add some secrets

1. Test connecting to it with code snippet




#### Links

https://docs.microsoft.com/en-us/azure/container-instances/container-instances-managed-identity

https://azure.microsoft.com/en-us/updates/aci-msi-preview/