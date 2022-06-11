# import requests
# import csv
# import json
import  boto3
from auth import ACCESS_KEY,SECRET_KEY

def pushS3():
    ''' pushing data to S3 bucket'''
    client=boto3.client('s3',aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

    #client.create_bucket(Bucket='william-airflow-blucket-2')
    with open("/Users/williamsalinas/airflow/dags/data_engineer_apple_job_postings.csv","rb") as f:
        client.upload_fileobj(f,"project-team10","data_engineer_apple_job_postings.csv")

    print("Upload Completed")