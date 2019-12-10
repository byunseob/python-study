import base64
import os
from datetime import datetime

import boto3 as boto3

# S3 권한 이 있어야함 아래 키도 해당 권한이 있는 IAM  액세스 시크릿키가 필요

S3_BUCKET = "BUCKET_NAME"
S3_KEY = "ACCESS_KEY"
S3_SECRET = "ACCESS_KEY"
S3_LOCATION = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)

s3 = boto3.client(
    "s3",
    aws_access_key_id=S3_KEY,
    aws_secret_access_key=S3_SECRET
)


def upload_file_to_s3(file, bucket_name, acl="public-read"):
    try:
        file_name = base64.urlsafe_b64encode(os.urandom(32)).rstrip(b'=').decode('utf-8')
        today = datetime.now().strftime('%Y-%m-%d')
        path_file_name = f'images/{today}/{file_name}'
        s3.upload_fileobj(
            file,
            bucket_name,
            path_file_name,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )

    except Exception as e:
        print("Something Happened: ", e)
        return e

    return "{}{}".format(S3_LOCATION, path_file_name)
