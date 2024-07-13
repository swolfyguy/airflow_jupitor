import requests
import json
import nbformat
from nbclient import NotebookClient
import subprocess

def get_jupyter_token():
    try:
        result = subprocess.run(['jupyter', 'server', 'list', '--json'], capture_output=True, text=True)
        output = result.stdout.strip()
        
        server_info = json.loads(output)
        if isinstance(server_info, dict):
            return server_info.get('token')
        
        print("Unexpected Jupyter server list output format.")
        print("Jupyter server list output:", output)
        return None
    except Exception as e:
        print(f"Error getting Jupyter token: {e}")
        print("Jupyter server list output:", output)
        return None

def execute_notebook_via_api(base_url, notebook_name):
    token = get_jupyter_token()
    
    if not token:
        print("Failed to get Jupyter token. Please ensure the server is running.")
        return None

    # Set up headers with authentication token
    headers = {"Authorization": f"Token {token}"}

    # Get the directory contents
    response = requests.get(base_url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to get directory contents: {response.status_code}")
        print(f"Response content: {response.text}")
        return None

    directory_data = response.json()
    
    # Find the notebook in the directory contents
    notebook_info = next((item for item in directory_data['content'] if item['name'] == notebook_name), None)
    if not notebook_info:
        print(f"Notebook {notebook_name} not found in directory")
        return None

    # Get the notebook content
    notebook_url = f"{base_url}/{notebook_name}"
    response = requests.get(notebook_url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to get notebook: {response.status_code}")
        print(f"Response content: {response.text}")
        return None

    notebook_data = response.json()

    # Try to load the notebook
    try:
        nb = nbformat.reads(json.dumps(notebook_data['content']), as_version=4)
    except Exception as e:
        print(f"Error parsing notebook: {e}")
        return None

    # Execute the notebook
    client = NotebookClient(nb, timeout=600)
    try:
        executed_nb = client.execute()
        print("Notebook executed successfully")
    except Exception as e:
        print(f"Error executing notebook: {e}")
        return None

    # Save the executed notebook back to the server
    payload = {
        "type": "notebook",
        "content": json.loads(nbformat.writes(executed_nb))
    }
    response = requests.put(notebook_url, headers=headers, json=payload)
    if response.status_code != 200:
        print(f"Failed to save notebook: {response.status_code}")
        print(f"Response content: {response.text}")
    else:
        print("Notebook saved successfully")

    return executed_nb

# Usage example
base_url = 'http://localhost:8888/api/contents/Notebooks'
notebook_name = 'notebook.ipynb'

executed_notebook = execute_notebook_via_api(base_url, notebook_name)