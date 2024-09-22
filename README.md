# breweries-case
Breweries Lake

## Table of Contents

- [About](#about)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Tests](#tests)
- [What comes next?](#what_comes_next)

## About <a name = "about"></a>

This project is a lakehouse for the breweries data. It's a test that consists in ingesting data from an API following the medallion architecture to display an aggregated view with the number of breweries per type and location.

## Prerequisites <a name = "getting_started"></a>

- [docker-compose](https://docs.docker.com/compose/)

## Getting Started <a name = "getting_started"></a>

First, we need to clone this repo:
```
git clone https://github.com/thiago-rente/breweries-case.git
```

The project is using Apache-Airflow to orchestrate, Python and Pyspark in DAG's tasks, MinIO as storage simulating Amazon S3 Buckets, Apache-Drill as (SQL Query Engine) to read Delta tables (gold layer) and Apache Superset to data visualization.

Link to resources:
- [Apache-Airflow](https://airflow.apache.org)
- [Apache-Spark](https://spark.apache.org)
- [Apache-Superset](https://superset.apache.org/)
- [Apache-Drill](https://drill.apache.org/)
- [MinIO](https://min.io)

## Usage <a name = "usage"></a>

Before we begin, let's check the containers used in the project:

* **minio**: S3 Object Storage.
    * image: docker.io/bitnami/minio:2024
    * ports: 9000 in services and 9001 to Web UI
    * user: brew:brew4321
    * UI: http://localhost:9001

![Screenshot: Minio](./screenshots/minio.png)

* **spark**: Large-scale, distributed processing system. The "spark" container is the "master".
    * image: docker.io/bitnami/spark:3.5.0
    * ports: 8080 to Web UI and 7077 in services
    * UI: http://localhost:8080

![Screenshot: Spark](./screenshots/spark.png)
 
 * **spark-worker-#**: Spark workers.
    * image: docker.io/bitnami/spark:3.5.0

* **airflow**: ETL/ELT Orchestrator.
    * image: apache/airflow:2.10.2rc1-python3.10
    * ports: 8081 to Web UI
    * user: airflow:airflow
    * UI: http://localhost:8081

![Screenshot: Apache Airflow](./screenshots/airflow.png)

* **jupyter**: Jupyter gives a development environment. I've made some tests to the medal steps using notebooks in this environment.
    * image: jupyter/pyspark-notebook:2023-10-20
    * ports: 8888 to Web UI
    * UI: http://localhost:8888

![Screenshot: Jupyter](./screenshots/jupyter.png)

* **drill**: Apache tool to access Delta Tables/Parquet Files using SQL Query Engine.
    * image: apache/drill:1.21.2
    * ports: 8047 to Web UI
    * UI: http://localhost:8047

![Screenshot: Apache Drill](./screenshots/drill.png)

* **superset**: Apache Superset is a tool to data visualization, generate reports and dashboards using data from Delta Tables.
    * image: apache/superset:994de1f-py310
    * ports: 8088 to Web UI
    * user: brew:brew4321
    * UI: http://localhost:8088

![Screenshot: Apache Superset](./screenshots/superset.png)

So to setup the environment, you can run these commands in a terminal (after going to the project folder):
```bash
docker compose build
```

```bash
docker compose up -d
```

To shutdown, use this command:
```bash
docker compose down
```

To connect to Drill via Apache Superset, a Database SQL Alchemy URI connection needs to be created, the connection string to connect drill is:
```
drill://drill:8047/s3.root?use_ssl=False
```

## Tests <a name = "tests"></a>

Before working in the ELT DAG in Apache Airflow, I used the Jupyter Lab environment to develop and test the medallion steps, validating the connections between the containers (Jupyter, spark, minio) and the integrity of data.

After that, when developing the DAG, I made some tests using pytest to check API request status, DAG's integrity, access to minio and spark and check the schema of data, validating the "key" columns of our project (location and brewery type).

The tests developed can be found in the directory "/airflow/tests" and to execute them in docker, run this command:
```bash
docker exec airflow pytest -v
```

## What comes next? <a name = "what_comes_next"></a>

In a productive environment, in addition to logs we can define other alert methods if any step of our ELT fails. Apache Airflow offers plugins and connections to group-chat softwares like Slack and Mail Servers. Whenever a dag fails, a message is sent to a group of people responsible to analyze the pipeline.