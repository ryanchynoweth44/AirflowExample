## Configuring your workspace for Airflow

In this demo we are working with Apache Airflow to create, schedule and monitor our data pipeline jobs. Since Apache Airflow does not support Windows we will be working of a Hyper-V VM with a Ubuntu operating system, please [create a virtual machine](./01_CreateUbuntuVM.md) if you have not done so. 


In this demo we will be coding in Python, and using the Anaconda distribution so lets start setting up a development environment.  

1. Download [visual studio code](https://code.visualstudio.com/docs/?dv=linux64_deb) for Ubuntu. Once the file is downloaded, simply run the file on your virtual machine to install.    

1. Next we will want to download and install the Python 3.7 version of [Anaconda](https://repo.anaconda.com/archive/Anaconda3-2018.12-Linux-x86_64.sh). We will be creating a virtual environment using Anaconda, for more information on how to create and use virtual environments with VS Code check out this [blog](https://ryansdataspot.com/2019/02/14/anaconda-environments-in-visual-studio-code/) I wrote. 


1. Open a terminal and create a conda environment to run Airflow. 
    ```
    conda create -n airflow python3.6
    ```

1. Activate your newly create conda environment. We will be running airflow through this conda environment.  
    ```
    conda activate airflow
    ```

1. Install apache airflow using pip. 
    ```
    pip install apache-airflow
    ```

Airflow is now installed and set up on your machine! Before we continue let's cover a few of basic details of apache airflow. 
- **Airflow Home Directory**: The airflow home directory contains the configuration, logs, and dags for your instance. If you are in development it will also contain the SQLite database. By default it is set to your root directory but we can set it to any directory we wish with the following command.  
    ```
    export AIRFLOW_HOME="<YOUR PATH HERE>"
    ```

- **Airflow Database**: Apache Airflow is built to interact with data using the SqlAlchemy library, and it is recommended to use either a MySQL or Postgres database backend. If you wish to use a database other than SQLite then you will need to set up a connection string in your `airflow.cfg` file, otherwise, it will initialize a SQLite Database.   
    ```
    # Set up SQLite Database
    airflow initdb
    ```

- **Airflow UI**: Airflow comes with a user interface to visualize, monitor, and execute your jobs. The first time you run the airflow webserver you will likely see the UI populated with many example DAGs. To get rid of the example DAGs locate your `airflow.cfg` file, and change the line `load_examples = True` to `load_examples = False`. 
    ```
    airflow webserver --port 8080
    ```

1. **Airflow Scheduler**: The airflow scheduler will automatically pick up and run any new DAGs in your `dag` folder i.e. dag folder located in your `AIRFLOW_HOME` directory. To run the scheduler in union with the UI, you will need to separate terminals both set with the same `AIRFLOW_HOME` directory, then simply execute the following command:   
    ```
    airflow scheduler
    ```








