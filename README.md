# Apache Airflow Example
This repository aims to provide an end to end example of [Apache Airflow](http://airflow.apache.org/index.html) for developers who are unfamiliar with it. Apache Airflow is a platform to programmatically author, schedule, and monitor workflows. Engineers can use airflow to create DAGs that execute tasks and visualize the pipeline.  


## Requirements
- Basic Knowledge of Python
- Linux VM 
- Anaconda Installation


## Blog
This demo is accompanied with a [blog](https://github.com/ryanchynoweth44/AirflowExample/blob/master/Docs/DataPipelinesUsingAirflow.md) discussing why data engineers and data scientists should use Apache Airflow to schedule, monitor, orchestrate, and create data pipelines. 


## Demo
The demo is broken into logical sections. Please complete in the following order:  
1. [Create Ubuntu VM](https://github.com/ryanchynoweth44/AirflowExample/blob/master/Docs/01_CreateUbuntuVM.md)
    - Note, I will be using a Hyper-V Virtual Machine on my local computer

1. [Configure workspace](./Docs/02_ConfigureWorkspace.md) 

1. [Create Hello World DAG](./Docs/03_HelloWorld.md)

1. [Create Pipeline using Azure ML](./Docs/04_AzureMLDataPipelines.md)

1. [Running Airflow with Docker](./Docs/05_RunningAirflowWithDocker.md)
