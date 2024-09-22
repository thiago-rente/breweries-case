from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark import SparkConf, SparkContext
import sys

spark = SparkSession(SparkContext(conf=SparkConf()).getOrCreate())

datetime = sys.argv[1]

# Read the JSON file from bronze bucket
source_bucket = "bronze"
prefix_bucket = "breweries"
source_path = f"s3a://{source_bucket}/{prefix_bucket}/{datetime}.json"

print(f"- Starting {source_path} read.")

bronze_data = spark.read.format('json').load(source_path)

print(f"- {source_path} read.")

# Write as a delta table the bronze data partitioned by country, state and city
target_bucket = "silver"
target_path = f"s3a://{target_bucket}/{prefix_bucket}/"

print(f"- Starting {target_path} write.")

bronze_data.write.mode('overwrite') \
    .format('delta') \
    .partitionBy("country", "state", "city") \
    .save(target_path)

print(f"- {target_path} finished.")
