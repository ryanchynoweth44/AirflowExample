## Apache Airflow Hello World

1. Create a working directory. In this repository, my working directory is [`code`.](../code)

1. In your working directory create a `dags` folder, with a subfolder called `tasks`. 

1. Our hello world example will simply print text to the command line and write a file to the local file system. Create a python script called `hello_world_tasks.py` and save it to the `tasks` folder. Paste the following code into the script.  
    ```python
    import datetime

    def print_world():
        print('world')



    def test_write_file():
        with open("test_file.txt", "w") as text_file:
            text_file.write("This is a test of Apache Airflow. - " + str(datetime.datetime.utcnow()))
    ```

1. Next we will create our DAG. Create a file called `hello_world.py` and save it to our `dag` folder.  

1. First lets import all the libraries that we would like to use in our DAG, including the `hello_world_tasks` that we just created. 
    ```python
    import datetime as dt
    import os, sys
    from airflow import DAG
    from airflow.operators.bash_operator import BashOperator
    from airflow.operators.python_operator import PythonOperator

    ## Custom data pipeline import
    from tasks import hello_world_tasks
    ```

1. Next we will want to set our default settings that is shared by all tasks in our DAG. 
    ```python
    current_dt = dt.datetime.utcnow()

    ## configure settings that are shared by all tasks in our DAG
    default_args = {
        'owner': 'Ryan Chynoweth',
        'start_date': current_dt,
        'retries': 1,
        'retry_delay': dt.timedelta(minutes=5),
    }
    ```
    DAGs have shared arguments that are available to all tasks that are a part of the DAG. One key argument is the `start_date` because when a DAG is run it is started from the start date. Meaning if a workflow is ran once a day, and you start the workflow 3 days after the specified start date then Airflow will check the database to see if the job was executed as expected for those three days. If it was not run, then it will run the DAG for the days that are missing in the database. Therefore, if it was started previously and only stopped for a few hours then it may not execute since those runs we executed, but a new job would execute all three days. 


1. Next we will create a DAG object that we can attach our tasks to. The DAG below will be executed every 5 minutes starting at the date time set in our default settings.
    ```python
    dag = DAG('hello_world_airflow_me', default_args=default_args, schedule_interval='*/5 * * * *')
    ```

1. Now we will create 5 tasks that we will attach to our DAG. There are two sleep tasks that will use the Bash functionality to have our DAG sleep for 5 seconds. Then there will be a Bash and a Python task to print text to the command line. Then finally we will write a file to the file system using another Python operator. 
    ```python
    # bash command to print text to command line
    print_hello = BashOperator(task_id='print_hello', bash_command='echo "hello"', dag=dag)
    # bash command to sleep
    sleep = BashOperator(task_id='sleep', bash_command='sleep 5', dag=dag)
    # python command that executes our print world function in our task script
    print_world = PythonOperator(task_id='print_world', python_callable=hello_world_tasks.print_world, dag=dag)
    # bash command to sleep
    sleep_two = BashOperator(task_id='sleep2', bash_command='sleep 5', dag=dag)
    # python command that writes file to file location using our task script
    print_file = PythonOperator(task_id='write_file', python_callable=hello_world_tasks.test_write_file, dag=dag)
    ```

1. The last thing we need to do before running the DAG is to order our tasks. The following line serializes our tasks by running them individually from left to right.  
    ```python
    print_hello >> sleep >> print_world >> sleep_two >> print_file
    ```

1. Now it is time to run our hello world DAG! Open two anaconda command prompts and activate the airflow conda environment that we created previously in both.  
    ```
    conda activate airflow
    ```

1. Next we need to set our airflow home directory to our working directory. Run the following command in both anaconda command prompts.  
    ```
    export AIRFLOW_HOME="<YOUR PATH HERE>"
    ```

1. Next we will initialize a SQLite Database by running this command in one of the anaconda commmand prompts.  
    ```
    airflow initdb
    ```

1. Next, open up `airflow.cfg` and change the line `load_examples = True` to `load_examples = False`. 

1. Start the web server by running the following command in one of the anaconda command prompts. Then navigate to `localhost:8080` using an internet browser.
    ```
    airflow webserver --port 8080
    ```

1. In the second command prompt run the airflow scheduler with the code below. The airflow scheduler will automatically pick up and run DAGs that are in our `dags` folder. Note that `dags` folder must be located in your `AIRFLOW_HOME` directory. 
    ```
    airflow scheduler
    ```


You have now developed and executed your first AIRFLOW DAG! For an end to end deployment in Azure check out the next step in our walkthrough [04_AzureAirflowPipeline.md]