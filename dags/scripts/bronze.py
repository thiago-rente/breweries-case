from airflow.hooks.S3_hook import S3Hook
from airflow.hooks.http_hook import HttpHook
import logging
import json

def save_file(datetime, file):
    s3 = S3Hook(aws_conn_id='conn_s3')

    bucket_name = "bronze"
    prefix = "breweries"
    filename = datetime + '.json'
    destination_file = bucket_name + "/" + prefix + "/" + datetime + ".json"

    s3.load_string(
        str(file),
        key= prefix + '/'+ filename,
        bucket_name=bucket_name,
        replace=True
    )
    
    logging.info(f"- s3://{destination_file} saved.")

def get_api():
    request = HttpHook(http_conn_id='conn_api', method='GET')
    return request.run(endpoint="breweries")

def bronze(datetime):
    breweries = get_api()

    if(breweries.status_code == 200):
        source_file = json.loads(breweries.text)
        save_file(datetime, source_file)
        logging.info(f"OK")
    else:
        logging.info(f"Request error")