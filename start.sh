#!/bin/bash

# Initialize the Airflow database
airflow db init

# Start Airflow scheduler and webserver
airflow scheduler &> /dev/null &
airflow webserver -p 8080 &> /dev/null