from auth import *

def run_s3_redshift():

    # module variables needed
    
    import botocore.session as bs
    import boto3

    #This query create the schema and tables
    sql_create_schema_and_tables ="""
    CREATE SCHEMA project;

    CREATE TABLE project.apple_data_engineer_jobs (
    job_id bigint IDENTITY(1,1),
    job_title varchar(500),
    job_location varchar(500),
    job_date_posted date,
    job_qualifications varchar(500),
    job_summary varchar(500),
    job_description varchar (500),
    job_education_experience varchar(500),
    Job_additional_qualifications varchar(500)
    ); """

    #This query wil drop the schema (and tables)
    sql_drop_schema="""
    DROP SCHEMA project cascade;
    """

    #the query
    sql_query="""COPY project.apple_data_engineer_jobs
    FROM 's3://project-team10/data_engineer_apple_job_postings.csv'
    REGION 'us-west-1'
    IAM_ROLE 'arn:aws:iam::891950201480:role/AmazonRedshiftRole'
    FORMAT CSV FILLRECORD
    TRUNCATECOLUMNS
    IGNOREHEADER 1;"""


    # create redshift data client
    session = bs.get_session()
    rsd_session = boto3.Session(botocore_session=session, region_name=aws_region)
    # UPDATE the session client below with the proper access keys
    rsd_client = rsd_session.client('redshift-data'
        , aws_access_key_id = rsd_access_key_id
        , aws_secret_access_key = rsd_secret_access_key)

    # define query execution and result retrieval methods using client
    def execute_query(client, sql_query, query_note=None):
        # use client to execute statement
        desc, query_id = None, None
        try:
            # show note of what query is running
            print('Currently running: {} query'.format(query_note))

            # UPDATE this object to include the parameters needed to retrieve data
            response = client.execute_statement(
                ClusterIdentifier = cluster_id,
                Database = redshift_db,
                DbUser = redshift_user,
                Sql = sql_query
            )

            # check status of query with the describe statement method
            query_id = response['Id']
        except:
            print('Client error: could not execute statement and retrieve results')
        return query_id

    execute_query(rsd_client,sql_drop_schema)
    execute_query(rsd_client,sql_create_schema_and_tables)
    execute_query(rsd_client,sql_query)
