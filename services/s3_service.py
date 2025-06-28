# services/s3_service.py
from typing import Optional

import boto3
from botocore.exceptions import ClientError

from config.settings import settings


class S3Service:
    def __init__(self):
        self.client = boto3.client(
            "s3",
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            region_name=settings.aws_region,
        )

    def presign_put_url(self, s3_key: str, expiration: int = 300) -> Optional[str]:
        try:
            response = self.client.generate_presigned_url(
                "put_object",
                Params={"Bucket": settings.s3_bucket, "Key": s3_key},
                ExpiresIn=expiration,
            )
            return response
        except ClientError:
            return None
