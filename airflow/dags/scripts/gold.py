from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark import SparkConf, SparkContext
import sys
import logging

spark = SparkSession(SparkContext(conf=SparkConf()).getOrCreate())

datetime = sys.argv[1]

# Read the Delta table from Silver bucket
source_bucket = "silver"
prefix_bucket = "breweries"
source_path = f"s3a://{source_bucket}/{prefix_bucket}/"

print(f"- Starting {source_path} read.")

# Write the aggregated view with quantity of breweries by type and location in a Delta table within gold bucket
agg_breweries_data = spark.sql(f'''
       SELECT
            country, state, city, brewery_type, count(1) as quantity
       FROM
          delta.`{source_path}`
       GROUP BY country, state, city, brewery_type
       ''')

print(f"- {source_path} read.")

print(agg_breweries_data.where("quantity > 1").head(5))

target_bucket = "gold"
target_path = f"s3a://{target_bucket}/{prefix_bucket}/"

print(f"- Starting {target_path} write.")

agg_breweries_data.write.mode('overwrite') \
    .format('delta') \
    .partitionBy("brewery_type", "country", "state", "city") \
    .save(target_path)

print(f"- {target_path} finished.")
