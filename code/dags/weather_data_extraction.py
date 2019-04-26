import datetime as dt
import os, sys
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from tasks import rest_tasks



current_dt = dt.datetime.utcnow()
start_date = dt.datetime(current_dt.year, current_dt.month, current_dt.day)

output_weather_data_path = "raw/weather_data/{}/{}/{}/{}/{}/weather_data.json".format(current_dt.year, current_dt.month, current_dt.day, current_dt.hour, current_dt.minute)

## configure settings that are shared by all tasks in our DAG
default_args = {
    'owner': 'Ryan Chynoweth',
    'start_date': start_date,
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=2),
}


## CRON Help - https://crontab.guru/
dag = DAG('weather_data_extraction', default_args=default_args, schedule_interval='*/30 * * * *')

get_weather_data = PythonOperator(task_id='get_weather_data', provide_context=True, python_callable=rest_tasks.get_aml_service_data, op_kwargs={'service_name': 'weatherdataextractor', 'output_path': output_weather_data_path}, dag=dag, catchup=False )

sleep = BashOperator(task_id="end_sleep", bash_command='sleep 10', dag=dag)

get_weather_data >> sleep