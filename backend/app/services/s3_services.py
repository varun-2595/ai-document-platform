import boto3
import os

s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_KEY_SECRET"),
    region_name=os.getenv("AWS_REGION")
)   

BUCKET_NAME = os.getenv("AWS_S3_BUCKET")

def upload_file_to_s3(file_path, s3_key):
    try:
        if not BUCKET_NAME:
            raise RuntimeError("AWS_S3_BUCKET is not configured")

        s3_client.upload_file(file_path, BUCKET_NAME, s3_key)
        return s3_key
    except Exception as e:
        print(f"Error uploading file to S3: {e}")
        return None
