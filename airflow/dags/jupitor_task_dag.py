from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import requests
import time

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
def run_notebook():
    jupyter_url = 'http://127.0.0.1:8888'
    token = '03e3a8a457ba90ececd4c17e9330c5d3dbec9046ef0d3534'
    notebook_path = '/path/to/your/notebook/airflow_test.ipynb'  # Update the path if necessary

    # API endpoints
    api_base = f'{jupyter_url}/api/contents'
    sessions_endpoint = f'{jupyter_url}/api/sessions'
    kernel_endpoint = f'{jupyter_url}/api/kernels'

    headers = {'Authorization': f'token {token}'}

    # Start a new session
    session_data = {
        'name': '',
        'path': notebook_path,
        'type': 'notebook',
        'kernel': {
            'id': '',
            'name': 'python3'
        }
    }
    response = requests.post(sessions_endpoint, headers=headers, json=session_data)
    response.raise_for_status()
    session = response.json()
    kernel_id = session['kernel']['id']

    # Execute the notebook
    execute_request = {
        'allow_stdin': False,
        'cell_timeout': None,
        'execute_all_cells': True,
        'kernel_name': 'python3',
    }
    execute_url = f'{jupyter_url}/api/kernels/{kernel_id}/execute'
    response = requests.post(execute_url, headers=headers, json=execute_request)
    response.raise_for_status()

    # Wait for the kernel to finish
    while True:
        response = requests.get(f'{kernel_endpoint}/{kernel_id}', headers=headers)
        response.raise_for_status()
        kernel_status = response.json().get('execution_state')
        if kernel_status == 'idle':
            break
        time.sleep(5)  # Wait for 5 seconds before checking again

    # Save the executed notebook
    save_url = f'{api_base}/{notebook_path}'
    response = requests.put(save_url, headers=headers)
    response.raise_for_status()

# Define the task using the PythonOperator
run_notebook_task = PythonOperator(
    task_id='run_notebook',
    python_callable=run_notebook,
    dag=dag,
)

# Set the task in the DAG
run_notebook_task
