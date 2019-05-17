# Deploying Airflow Solutions in Azure

So far in this walkthrough we have developed and tested our DAGs locally by running airflow commands in the command line. Hopefully by now you have a solid understanding of some of the Apache Airflow capabilities and how to develop data solutions using it, but how do you get from your Ubuntu VM to production? My favorite way of deploying an Airflow solution is using [Docker](https://www.docker.com/). 

When deploying Apache Airflow with Docker the current standard image is `puckel/docker-airflow`, and the repository is available on [GitHub](https://github.com/puckel/docker-airflow). The main way that developers will use the `puckel/docker-airflow` image is to deploy the airflow application by following the instructions from GitHub README, then use docker volumes to persist the DAG files to the Docker containers. Volumes are a great way to manage your airflow DAGs because they easily allow users to test jobs on different environments and simply move the scripts from one volume to another to add it to the environment and get picked up by the airflow scheduler. We will walk through a Volume Deployment in the [next section](./07_DeployAirflowWithVolumes.md)

Another way to deploy Apache Airflow with `puckel/docker-airflow` is to add the DAG files to the container image creation. This would force developers to have a new version of the container each time you change a data pipeline. Lets start deploying airflow by adding our DAG to the Docker image build.


## Local Custom Docker Build for Airflow

1. In our `AirflowContainer` folder we need to create a `Dockerfile` to build our image. Paste the following into the `Dockerfile`.
    ```
    FROM puckel/docker-airflow

    ARG AIRFLOW_VERSION=1.10.2
    ARG AIRFLOW_HOME=/usr/local/airflow
    ARG AIRFLOW_DEPS=""
    ARG PYTHON_DEPS=""

    COPY /dags /usr/local/airflow/dags
    COPY requirements.txt /usr/local/airflow

    WORKDIR ${AIRFLOW_HOME}
    RUN pip install --user -r requirements.txt
    ```

    In this case we are starting with the standard `puckel/docker-airflow` airflow image, then we simply want to copy our DAGs and our custom requirements into the Airflow Home Direcory. Then once those files are copied over we will run a pip install using our `requirements.txt` file that we will create in the next step.  

1. Now we want to create our `requirements.txt` file with the following Azure dependencies. 
    ```
    azureml-sdk==1.0.39
    azure-datalake-store==0.0.45
    ```

1. The last file we need to create is a `docker-compose-LocalExecutor.yml` file that we will run to deploy and run our Docker container. You will notice that this file is pulled from the [`puckel/docker-airflow`](https://github.com/puckel/docker-airflow) with one change. 
    ```
    version: '2.1'
    services:
        postgres:
            image: postgres:9.6
            environment:
                - POSTGRES_USER=airflow
                - POSTGRES_PASSWORD=airflow
                - POSTGRES_DB=airflow

        webserver:
            #image: puckel/docker-airflow:1.10.2
            image: <THE_NAME_OF_YOUR_CUSTOM_DOCKER_CONTAINER_HERE>:lastest
            restart: always
            depends_on:
                - postgres
            environment:
                - LOAD_EX=n
                - EXECUTOR=Local
            volumes:
                - ./dags:/usr/local/airflow/dags
                # Uncomment to include custom plugins
                # - ./plugins:/usr/local/airflow/plugins
            ports:
                - "8080:8080"
            command: webserver
            healthcheck:
                test: ["CMD-SHELL", "[ -f /usr/local/airflow/airflow-webserver.pid ]"]
                interval: 30s
                timeout: 30s
                retries: 3
    ```

1. Now open a command prompt, navigate to the `AirflowContainer` directory, and run the following command to build your Docker container. 
    ```
    sudo docker build -t airflow_docker .
    ```

1. Let's run the newly created image locally on our machine. Just make sure that the image name is provided in your `docker-compose-LocalExecutor.yml`. 
    ```
    docker-compose -f docker-compose-LocalExecutor.yml up -d
    ```

1. Now check out your Airflow container running on [localhost:8080](http://localhost:8080)!


## Deploy Airflow with Azure Pipelines

We have gone through all the steps manually to build and run a docker image on our local machines. Lets try deploying our container to Azure Container Instance (ACI) using the Azure Pipelines inside of Azure DevOps. Please note that we are deploying to ACI for the sake of this demo, I typically recommend users deploy to ACI for dev and test environments and use an Azure Kubernetes Service for production deployments. 

1. Create Azure Resources

1. Add your code to source control

1. Create a build

1. 

