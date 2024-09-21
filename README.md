# breweries-case
Breweries Lake

## Table of Contents

- [About](#about)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Resources](#resources)
- [etc.](#licence)

## About <a name = "about"></a>

This project is a lakehouse for the breweries data. It's a test that consists in ingesting data from an API following the medallion architecture to display an aggregated view with the number of breweries per type and location.

## Prerequisites <a name = "getting_started"></a>

- [docker-compose](https://docs.docker.com/compose/)

## Getting Started <a name = "getting_started"></a>

The project is using Apache-Airflow to orchestrate, Python and Pyspark in DAG's tasks, MinIO as storage, Apache-Drill as (SQL Query Engine) and Apache Superset to data visualization.

Link to resources:
- [Apache-Airflow](https://airflow.apache.org)
- [Apache-Spark](https://spark.apache.org)
- [Apache-Superset](https://superset.apache.org/)
- [Apache-Drill](https://drill.apache.org/)
- [MinIO](https://min.io)
