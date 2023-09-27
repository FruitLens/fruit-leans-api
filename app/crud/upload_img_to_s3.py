import boto3
from fastapi import UploadFile

from app.core.config import settings


async def upload_img_to_s3(file: UploadFile, file_name: str) -> bool:
    try:
        print("upload image to S3")
        s3 = boto3.client("s3")
        s3.put_object(
            Bucket=settings.S3_BUCKET_NAME,
            Key="users_images/" + file_name,
            Body=file.file,
        )
        return True
    except Exception as e:
        print(e)
        return False
