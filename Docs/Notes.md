## Installation

1. Create Conda Environment.

1. Install airflow.
    ```
    pip install apache-airflow
    ```

1. Next set your airflow home to the directory you with. Please note that the dags will need to be in this AIRFLOW_HOME folder in order for them to be picked up by the airflow scheduler.  
    ```
    export AIRFLOW_HOME="~/Documents/git/AirflowExample/code"
    ```

1. Initialize the database. By default it will be SQLlite but in production you can use MySQL or PostgresSQL.
    ```
    airflow initdb
    ```

1. You can start the web server by running the following command. There is a built in UI to start, stop, and monitor the tasks you create. 
    ```
    airflow webserver --port 8080
    ```
    The UI looks like the image below. 


## Workflows

Workflows are represented by Directed Acyclic Graphs (DAGs) written in Python. Tasks are subcomponents of a DAG and are directional and can be dependent on each other to execute your python scripts as designed. 


DAGs have shared arguments that are available to all tasks that are a part of the DAG. One key argument is the `start_date` because when a DAG is run it is started from the start date. Meaning if a workflow is ran once a day, and you start the workflow 3 days after the specified start date then Airflow will check the database to see if the job was executed as expect and if not it will run the DAG for the days that it was missing. Therefore, if it was started previously and only stopped for a few hours then it may not execute since those runs we executed, but a new job would execute all three days. 

### Tasks 
Tasks are represented by operators that either perform actions, transfer data, or sense if something has been done. Task actions can be bash scripts or python functions, task transfers are simply table or file copies, and sensors simply check if tasks have been executed or data exists.


## Easy Example

1. Download this repo 

1. Navigate to the code repo.

1. Run the following command in the terminal to test the DAG locally to ensure there are no errors.
    ```
    python ./dags/hello_world.py
    ```
1. Now lets run the our dag! In order to do so you must turn on the scheduler. In a second terminal:
    - activate the conda environment
    - set the airflow home variable for this terminal 
    - run `airflow scheduler`




## Deleting Example DAGs
In the `airflow.cfg` file there is a line that says `load_examples = True` we will want to set this variable to `Flase`.  


## Making Code Edits

Note that changes to your dags are automatically picked up by the scheduler. Take for example the `hello_world_tasks.py` file, there is a function called `test_write_file`. To see code changes automatically get picked up simply change the string that we are writing to file. By default we are writing a datetime stamp, but this can be anything you want.  

## DevOps
Since Airflow is simply a solution and a web server, the deployment is like any other web app deployment. 


## Docker Link
https://medium.com/@shahnewazk/dockerizing-airflow-58a8888bd72d