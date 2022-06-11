from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python_operator import PythonOperator
from s3_upload import pushS3
from s3_to_redshift import run_s3_redshift
import boto3
import botocore.session as bs

from Apple_Job_scrapper_airflow import run_scraper

default_args = {
    'owner': 'Airflow',
    'start_date': datetime(2022, 6, 8),
    'retries': 1,
    'retry_delay': timedelta(seconds=5)
}

with DAG("S3_UPLOAD",default_args=default_args, schedule_interval="@daily", catchup=False) as dag:
    #t1=PythonOperator(task_id="S3-Using-Python", python_callable=pushS3)

    t1=PythonOperator(task_id="Running-Scrapper-Apple-Jobs", python_callable=run_scraper)
    t2=PythonOperator(task_id="S3-Using-Python", python_callable=pushS3)
    t3=PythonOperator(task_id="Redshift-Using-Python", python_callable=run_s3_redshift)

    t1 >> t2 >> t3