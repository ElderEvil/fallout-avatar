import io
import json

from minio import Minio
from minio.error import S3Error

from config import settings

from exceptions import BucketNotFoundError, FileDownloadError, FileUploadError


PUBLIC_POLICY_TEMPLATE = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {"AWS": ["*"]},
            "Action": [
                "s3:GetBucketLocation",
                "s3:ListBucket",
                "s3:ListBucketMultipartUploads",
            ],
            "Resource": [],
        },
        {
            "Effect": "Allow",
            "Principal": {"AWS": ["*"]},
            "Action": [
                "s3:AbortMultipartUpload",
                "s3:DeleteObject",
                "s3:ListMultipartUploadParts",
                "s3:PutObject",
                "s3:GetObject",
            ],
            "Resource": [],
        },
    ],
}


class MinioService:
    def __init__(self):
        self.client = Minio(
            f"{settings.MINIO_HOST}:{settings.MINIO_CUSTOM_PORT}",
            access_key=settings.MINIO_ROOT_USER,
            secret_key=settings.MINIO_ROOT_PASSWORD,
            secure=False,  # True if using https
        )
        self.default_bucket_name = "fastapi-minio"
        self._ensure_bucket_exists(self.default_bucket_name)

    @staticmethod
    def _get_public_policy(bucket_name: str) -> str:
        policy = PUBLIC_POLICY_TEMPLATE.copy()
        policy["Statement"][0]["Resource"] = [f"arn:aws:s3:::{bucket_name}"]
        policy["Statement"][1]["Resource"] = [f"arn:aws:s3:::{bucket_name}/*"]
        return json.dumps(policy)

    def _ensure_bucket_exists(self, bucket_name: str) -> None:
        try:
            if not self.client.bucket_exists(bucket_name):
                self.client.make_bucket(bucket_name)
        except S3Error as e:
            error_msg = f"Error creating bucket {bucket_name}: {e}"
            raise BucketNotFoundError(error_msg) from e

    def _ensure_bucket_policy(self, bucket_name: str) -> None:
        """
        Ensure that the bucket has the correct policy set.
        :param bucket_name: The name of the bucket to check.
        """
        if bucket_name not in settings.MINIO_PUBLIC_BUCKET_WHITELIST:
            return
        expected_policy = self._get_public_policy(bucket_name)
        try:
            current_policy = self.client.get_bucket_policy(bucket_name)
        except S3Error as e:
            if "NoSuchBucketPolicy" in str(e):
                current_policy = None
            else:
                error_msg = f"Error getting bucket policy for {bucket_name}: {e}"
                raise BucketNotFoundError(error_msg) from e

        if current_policy != expected_policy:
            try:
                self.client.set_bucket_policy(bucket_name, expected_policy)
            except S3Error as e:
                error_msg = f"Error setting bucket policy for {bucket_name}: {e}"
                raise BucketNotFoundError(error_msg) from e

    def upload_file(
        self, *, file_data: bytes, file_name: str, bucket_name: str | None = None
    ) -> str:
        bucket_name = bucket_name or self.default_bucket_name
        self._ensure_bucket_exists(bucket_name)
        try:
            result = self.client.put_object(
                bucket_name,
                file_name,
                io.BytesIO(file_data),
                length=len(file_data),
                content_type="image/png",
            )
            return (
                self.public_url(file_name=file_name, bucket_name=bucket_name)
                if bucket_name in settings.MINIO_PUBLIC_BUCKET_WHITELIST
                else result.object_name
            )
        except S3Error as e:
            error_msg = f"Error uploading file to MinIO: {e}"
            raise FileUploadError(error_msg) from e

    def download_file(self, *, file_name: str, bucket_name: str | None = None) -> bytes:
        bucket_name = bucket_name or self.default_bucket_name
        try:
            response = self.client.get_object(bucket_name, file_name)
            return response.read()
        except S3Error as e:
            error_msg = f"Error downloading file from MinIO: {e}"
            raise FileDownloadError(error_msg) from e

    def public_url(self, *, file_name: str, bucket_name: str | None = None) -> str:
        bucket_name = bucket_name or self.default_bucket_name
        self._ensure_bucket_policy(bucket_name)
        return f"{settings.MINIO_HOST}:{settings.MINIO_CUSTOM_PORT}/{bucket_name}/{file_name}"


def get_minio_client() -> MinioService:
    return MinioService()
