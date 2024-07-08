# Getting started with Apache Airflow

## Prerequisites

- Docker
- Docker Compose

### Install Docker

Follow the [Docker installation guide](https://docs.docker.com/get-docker/) to install Docker on your system.

### Install Docker Compose

Docker Compose is included in Docker Desktop for Windows and Mac. For Linux, you can install it separately by following the [Docker Compose installation guide](https://docs.docker.com/compose/install/).

## Project Setup

### Clone the Repository

First, clone the repository from GitHub:
https://github.com/swolfyguy/airflow_jupitor.git



### Build and Run the Project

1. **Initialize Airflow**

   To set up Airflow, run the following command:


   This will initialize the Airflow database and create the necessary user.

2. **Start Airflow Services**

   After initializing the database, start the Airflow services:


   This will start the Airflow webserver, scheduler, and other necessary services.

### Access Airflow

You can access the Airflow web interface by navigating to `http://localhost:8080` in your web browser.

### Default Credentials

- **Username:** airflow
- **Password:** airflow

### Additional Information

- For more details on the project structure, see the `dags` folder for example DAGs.
- The `docker-compose.yml` file contains the configuration for all services, including Airflow, PostgreSQL, and Jupyter.

### Made with ❤️ by @sandeep