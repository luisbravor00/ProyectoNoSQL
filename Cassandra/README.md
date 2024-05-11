# Cassandra Project
## Setup a python virtual environment
    python -m venv ./venv
    .\venv\Scripts\Activate.ps1
    pip install -r requirements.txt

## Create and launch a Cassandra Container (docker)
    docker run --name cassandra_project -p 9042:9042 -d cassandra
    docker start cassandra_project

## Create random data and save it in a cql file
    python ./tools/populate.py
    * And verify if the data was created correctly *

## Copy the data to the container
    docker cp tools/data.cql cassandra_project:/root/data.cql

    * Run the client.py to create the schema if it's the first time you are creating the database *
    python client.py

    * When you run the client, don't do anything else *
    docker exec -it cassandra_project cqlsh

    * And then inside of cqlsh *
    USE hospital;
    SOURCE '/root/data.cql'

## Run the client.py normally
    * You have a login inside the client so you can only access with the specific user and password *
    user: admin
    password: 123
