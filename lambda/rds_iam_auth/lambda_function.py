"""Simple Lambda."""
import pymysql
import boto3
import os
import sys
import logging

ENDPOINT = "test-rds-iam-auth.caa2bd2defxp.ap-northeast-1.rds.amazonaws.com"
PORT = "3306"
USR = "lambda-role-for-rds"
REGION = "ap-northeast-1"
DBNAME = "lag_cv"
os.environ['LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN'] = '1'

logger = logging.getLogger()
[logger.removeHandler(h) for h in logger.handlers]
log_format = "%(asctime)-15s [%(funcName)s] %(message)s"
stdout_handler = logging.StreamHandler(stream=sys.stdout)
stdout_handler.setFormatter(logging.Formatter(log_format))
logger.addHandler(stdout_handler)
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    """Main func."""
    # gets the credentials from .aws/credentials
    # session = boto3.Session(profile_name='default')
    client = boto3.client('rds')
    token = client.generate_db_auth_token(
        DBHostname=ENDPOINT, Port=PORT, DBUsername=USR, Region=REGION)

    conn = get_connection(token)
    # logger.info(conn.host, conn.user)

    try:
        with conn.cursor() as cursor:
            cursor.execute("""SELECT * FROM job_execution;""")
            query_results = cursor.fetchall()
            logger.info(query_results)
    except Exception as e:
        logger.info("Database connection failed due to {}".format(e))

    return {"result": query_results}


def get_connection(token):
    """Get connection."""
    logger.info("Get connection.")
    conn = pymysql.connect(
        host=ENDPOINT, user=USR, passwd=token, port=int(PORT), db=DBNAME,
        cursorclass=pymysql.cursors.DictCursor,
        ssl={'ca': 'rds-ca-2019-root.pem'}
    )
    logger.info("Successfully getting the connection.")
    return conn
