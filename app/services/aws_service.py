from typing import Annotated, Protocol

import boto3
from botocore.exceptions import ClientError
from fastapi import Depends

from app.config import Settings, get_settings
from app.data.errors import CouldNotUploadFileError, CouldNotDeleteFileError


class AWSServiceInterface(Protocol):
    async def upload_file_to_s3(self, file_name: str, file) -> str:
        ...

    async def delete_file_from_s3(self, file_name: str):
        ...


class AWSService:

    def __init__(self, setting: Annotated[Settings, Depends(get_settings)]):
        self.settings = setting

    async def upload_file_to_s3(self, file_name: str, file) -> str:
        aws_bucket = self.settings.aws_bucket
        aws_region = self.settings.aws_region
        s3_client = boto3.client('s3', aws_access_key_id=self.settings.aws_key,
                                 aws_secret_access_key=self.settings.aws_secret)
        try:
            s3_client.upload_fileobj(file, aws_bucket, f"images/{file_name}")
            url = f"https://{aws_bucket}.s3.{aws_region}.amazonaws.com/images/{file_name}"
            return url
        except ClientError as e:
            raise CouldNotUploadFileError(e)

    async def delete_file_from_s3(self, file_name: str):
        aws_bucket = self.settings.aws_bucket
        s3_client = boto3.client('s3', aws_access_key_id=self.settings.aws_key,
                                 aws_secret_access_key=self.settings.aws_secret)
        try:
            response = s3_client.delete_object(Bucket=aws_bucket, Key=f"images/{file_name}")
        except ClientError as e:
            raise CouldNotDeleteFileError(e)
        else:
            return response
