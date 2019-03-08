import os, sys
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

# os.path.abspath('')
# from scripts import test_print

start_dt = datetime.utcnow() + timedelta(hours=1)

default_args = {
    'owner': 'Ryan',
    'depends_on_past': False,
    'start_date': start_dt,
    'email': ['rchynoweth@10thmagnitude.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5), 
    # 'queue': bash_queue,
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': start_dt + timedelta(days=7)
}


dag = DAG('demo', default_args=default_args, schedule_interval=timedelta(minutes=30))


task_one = PythonOperator(task_id='test_print', python_callable=test_print.test_write_file, dag=dag)
# task_two = PythonOperator(task_id='test_print', python_callable=test_print.test_write_file, dag=dag)
# task_three = PythonOperator(task_id='test_print', python_callable=test_print.test_write_file, dag=dag)


## The four following commands are equivalent
## This means that task_two will depend on the completion of tast_one
# task_one.set_downstream(task_two) 
# task_two.set_upstream(task_one)
# task_one >> task_two
# task_two << task_one

## it is possible to chain them in a single line 
# task_one >> task_two >> task_three

