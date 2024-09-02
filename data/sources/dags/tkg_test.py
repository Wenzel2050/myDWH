from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime

# Define the DAG
dag = DAG(
    'tkg-test',
    description='A simple tutorial DAG',
    schedule_interval='*/3 * * * *',
    start_date=datetime(2023, 3, 22),
    catchup=False
)

# Define the BashOperator task
hello_world_task = BashOperator(
    task_id='hello_world_task',
    bash_command='python -c "print(\'Hello, world!\')"',
    dag=dag
)

hello_world_task_2 = BashOperator(
    task_id='hello_world_task_2',
    bash_command='python -c "print(\'Nochmal, world!\')"',
    dag=dag
)#

sqlplus = BashOperator(
    task_id='hello_world_task_3',
    bash_command='/opt/airflow/dags/sqlplus',
    dag=dag
)

# Define the task dependencies
hello_world_task >> hello_world_task_2 >> sqlplus
