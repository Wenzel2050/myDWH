from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.docker_operator import DockerOperator
from datetime import datetime
from docker.types import Mount

# Define the DAG
dag = DAG(
    'dbt-test',
    description='A simple tutorial DAG',
    schedule_interval='*/3 * * * *',
    start_date=datetime(2023, 3, 22),
    catchup=False
)

hop_task = DockerOperator(
    task_id='doitwithhop',
    image='apache/hop',
    container_name='doitwithhop',
    environment={
        "HOP_LOG_LEVEL": "Basic",
        "HOP_FILE_PATH": "${PROJECT_HOME}/todatest.hpl",
        "HOP_PROJECT_FOLDER": "/project",
        "HOP_PROJECT_NAME": "todatest",
        "HOP_RUN_CONFIG": "local"
        },
    mounts=[
        Mount(
            source='/home/peterf/work/sources/toda/data/sources/hop',
            target='/project',
            type='bind'
        )
    ],
    auto_remove=True,
    dag=dag
)

dbt_task = DockerOperator(
    task_id='doitwithdbt',
    image='toda-dbt',
    container_name='doitwithdbt',
    command='dbt --help',
    auto_remove=True,
    dag=dag
)


# Define the task dependencies
hop_task >> dbt_task 
