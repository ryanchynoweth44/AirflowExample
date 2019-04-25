import datetime as dt
import os, sys
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

from tasks import hello_world_tasks


current_dt = dt.datetime.utcnow()

## configure settings that are shared by all tasks in our DAG
default_args = {
    'owner': 'Ryan Chynoweth',
    'start_date': current_dt,
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=5),
}



## Create a DAG Object to attach our tasks to
## CRON Help - https://crontab.guru/#0_*_*_*_*  i.e. run every 5 minutes
dag = DAG('hello_world_airflow_me', default_args=default_args, schedule_interval='*/5 * * * *')
## each task will need to be indented. 
## alternatively we could attach each task separately

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


print_hello >> sleep >> print_world >> sleep_two >> print_file