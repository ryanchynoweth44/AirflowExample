import datetime as dt
import os, sys
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

from tasks import hello_world_tasks


current_dt = dt.datetime.now()

## configure settings that are shared by all tasks in our DAG
default_args = {
    'owner': 'Ryan Chynoweth',
    'start_date': current_dt,
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=5),
}



## Create a DAG Object to attach our tasks to
## CRON Help - https://crontab.guru/#0_*_*_*_*  i.e. run every 5 minutes
dag = DAG('hellow_world_airflow_me', default_args=default_args, schedule_interval='*/5 * * * *')
## each task will need to be indented. 
## alternatively we could attach each task separately

print_hello = BashOperator(task_id='print_hello', bash_command='echo "hello"', dag=dag)
sleep = BashOperator(task_id='sleep', bash_command='sleep 5', dag=dag)
print_world = PythonOperator(task_id='print_world', python_callable=hello_world_tasks.print_world, dag=dag)


print_hello >> sleep >> print_world