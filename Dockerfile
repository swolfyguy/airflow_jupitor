# Use an official Airflow image as a parent image
FROM apache/airflow:2.3.0-python3.8

# Set environment variables
ENV AIRFLOW_HOME=/usr/local/airflow

# Install necessary dependencies
USER root
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install additional Python packages if needed
RUN pip install apache-airflow[postgres,crypto,kubernetes]

RUN pip install papermill

# Copy the Airflow configuration files
COPY airflow.cfg ${AIRFLOW_HOME}/airflow.cfg
COPY dags ${AIRFLOW_HOME}/dags

# Set the working directory
WORKDIR ${AIRFLOW_HOME}

# Run Airflow webserver and scheduler
CMD ["airflow", "webserver"]
CMD ["airflow", "scheduler"]
