import os

import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

from app.data.errors import CouldNotUploadFileError, CouldNotDeleteFileError

load_dotenv()

aws_bucket = os.getenv('AWS_BUCKET')
aws_region = os.getenv('AWS_REGION')


async def upload_file_to_s3(file_name: str, file, bucket: str = aws_bucket) -> str:
    s3_client = boto3.client('s3', aws_access_key_id=os.getenv('AWS_KEY'),
                             aws_secret_access_key=os.getenv('AWS_SECRET'))
    try:
        s3_client.upload_fileobj(file, bucket, f"images/{file_name}")
        url = f"https://{aws_bucket}.s3.{aws_region}.amazonaws.com/images/{file_name}"
        return url
    except ClientError as e:
        raise CouldNotUploadFileError(e)


async def delete_file_from_s3(file_name: str, bucket: str = aws_bucket):
    s3_client = boto3.client('s3', aws_access_key_id=os.getenv('AWS_KEY'),
                             aws_secret_access_key=os.getenv('AWS_SECRET'))
    try:
        response = s3_client.delete_object(Bucket=bucket, Key=f"images/{file_name}")
    except ClientError as e:
        raise CouldNotDeleteFileError(e)
    else:
        return response
