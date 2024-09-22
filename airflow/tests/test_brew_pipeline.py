import pytest
import requests
import json
import os
from unittest.mock import MagicMock, call
from jsonschema import validate
from pyspark.sql import SparkSession
from airflow.models import DagBag, Connection
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

@pytest.fixture()
def dag_bag():
    return DagBag()

@pytest.fixture()
def connect_api():
    url = 'http://api.openbrewerydb.org/breweries'
    response = requests.get(url)
    return response

# Test if dag is OK
def test_dag_loaded(dag_bag):
    dag = dag_bag.get_dag(dag_id='breweries_pipeline')
    assert dag is not None

# Test if API is accessible
def test_http_connection(connect_api):
    assert connect_api.status_code == 200

# Test if minio is accessible
def test_minio_access():
    conn_minio = Connection(
        conn_id="test_s3",
        conn_type="aws",
        extra=json.dumps({
            "aws_access_key_id": "brew",
            "aws_secret_access_key": "brew4321",
            "endpoint_url": "http://minio1:9000/"
        })
    )

    os.environ["AIRFLOW_CONN_TEST_S3"] = conn_minio.get_uri()
    minio = S3Hook(aws_conn_id='test_s3')
    assert minio.check_for_bucket("bronze")

# Test if spark is accessible
def test_spark_access():
    spark = SparkSession.builder.master("spark://spark1:7077").appName("test").getOrCreate()
    assert isinstance(spark, SparkSession)

# Test json schema
def test_json_schema(connect_api):
    schema = {
        "type": "object",
        "properties": {
            "id": {"type": "string"},
            "name": {"type": ["string", "null"]},
            "brewery_type": {"type": "string"},
            "address_1": {"type": ["string", "null"]}, 
            "address_2":{"type": ["string", "null"]},
            "address_3":{"type": ["string", "null"]},
            "city":{"type": "string"},
            "state_province":{"type": ["string", "null"]},
            "postal_code":{"type": ["string", "null"]},
            "country":{"type": "string"},
            "longitude":{"type": ["string", "null"]},
            "latitude":{"type": ["string", "null"]},
            "phone":{"type": ["string", "null"]},
            "website_url":{"type": ["string", "null"]},
            "state":{"type": "string"},
            "street":{"type": ["string", "null"]}
        },
        "required": ["id", "brewery_type", "city", "country", "state"],
    }

    for brew in json.loads(connect_api.text):
        assert validate(instance=brew, schema=schema) is None