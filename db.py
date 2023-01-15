import boto3
import pymysql
import json
import os
from botocore.exceptions import ClientError


def connect():
    try:
        connection = pymysql.connect(
            host='wetube-rds-proxy.proxy-ce8ks8bvrmly.ap-northeast-2.rds.amazonaws.com',
            user=os.environ['username'],
            password=os.environ['password'],
            db=os.environ['db_name'],
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            ssl={"use": True}
        )
    except pymysql.MySQLError as e:
        return e

    return connection
