from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator

from scripts.bronze import bronze

with DAG(dag_id='breweries_pipeline',
         default_args={'owner':'airflow'},
         schedule_interval=None,
         start_date=days_ago(2),
         tags=['etl', 'breweries', 'lake']) as dag:

     execution_date_time = '{{ ts_nodash }}'

     start = DummyOperator(task_id="start", dag=dag)

     bronze_step = PythonOperator(
        task_id="bronze_step",
        python_callable=bronze,
        op_kwargs={'datetime': execution_date_time},
        dag=dag
     )

     silver_step = SparkSubmitOperator(
        task_id='silver_step',
        conn_id='conn_spark',
        application="/opt/airflow/dags/scripts/silver.py",
        application_args=[execution_date_time], #parameters to the pyspark job via sys.args
        name="bronze_to_silver",
        conf={
            "spark.sql.extensions": "io.delta.sql.DeltaSparkSessionExtension",
            "spark.sql.catalog.spark_catalog": "org.apache.spark.sql.delta.catalog.DeltaCatalog",
            "spark.hadoop.fs.s3a.proxy.host": "minio1",
            "spark.hadoop.fs.s3a.proxy.port": "9000",
            "spark.hadoop.fs.s3a.access.key": "brew",
            "spark.hadoop.fs.s3a.secret.key": "brew4321",
            "spark.hadoop.fs.s3a.path.style.access": "true",
            "spark.hadoop.fs.s3a.connection.ssl.enabled": "false",
            "spark.hadoop.fs.s3a.impl": "org.apache.hadoop.fs.s3a.S3AFileSystem",
            "spark.hadoop.fs.s3a.connection.estabilish.timeout": "5000"
        },
        packages="org.apache.hadoop:hadoop-aws:3.3.4,io.delta:delta-spark_2.12:3.2.0"
     )

     gold_step = SparkSubmitOperator(
        task_id='gold_step',
        conn_id='conn_spark',
        application="/opt/airflow/dags/scripts/gold.py",
        application_args=[execution_date_time],
        name="silver_to_gold",
        conf={
            "spark.sql.extensions": "io.delta.sql.DeltaSparkSessionExtension",
            "spark.sql.catalog.spark_catalog": "org.apache.spark.sql.delta.catalog.DeltaCatalog",
            "spark.hadoop.fs.s3a.proxy.host": "minio1",
            "spark.hadoop.fs.s3a.proxy.port": "9000",
            "spark.hadoop.fs.s3a.access.key": "brew",
            "spark.hadoop.fs.s3a.secret.key": "brew4321",
            "spark.hadoop.fs.s3a.path.style.access": "true",
            "spark.hadoop.fs.s3a.connection.ssl.enabled": "false",
            "spark.hadoop.fs.s3a.impl": "org.apache.hadoop.fs.s3a.S3AFileSystem",
            "spark.hadoop.fs.s3a.connection.estabilish.timeout": "5000"
        },
        packages="org.apache.hadoop:hadoop-aws:3.3.4,io.delta:delta-spark_2.12:3.2.0"
     )

     end = DummyOperator(task_id="end", dag=dag)

     start >> bronze_step >> silver_step >> gold_step >> end