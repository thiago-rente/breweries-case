from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark import SparkConf, SparkContext
import sys

spark = SparkSession(SparkContext(conf=SparkConf()).enableHiveSupport().getOrCreate())

datetime = sys.argv[1]

source_bucket = "bronze"
prefix_bucket = "breweries"
source_path = f"s3a://{source_bucket}/{prefix_bucket}/{datetime}.json"

bronze_data = spark.read.format('json').load(source_path)

target_bucket = "silver"
target_path = f"s3a://{target_bucket}/{prefix_bucket}/"

bronze_data.write.mode('overwrite') \
    .format('delta') \
    .partitionBy("country", "state", "city") \
    .save(target_path)