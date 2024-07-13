from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import requests
import time
import papermill as pm

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'execute_jupyter_notebook',
    default_args=default_args,
    description='A DAG to execute a local Jupyter notebook',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 1, 1),
    catchup=False,
)

# Define the Python function to execute the notebook
def run_notebook(**kwargs):
    pm.execute_notebook(
        input_path='/opt/airflow/dags/notebooks/notebook.ipynb',  # Input notebook
        output_path='/opt/airflow/dags/notebooks/notebook_output.ipynb',  # Output notebook
        kernel_name='python3'
    )

# Define the task using the PythonOperator
run_notebook_task = PythonOperator(
    task_id='run_notebook',
    python_callable=run_notebook,
    dag=dag,
)

# Set the task in the DAG
run_notebook_task