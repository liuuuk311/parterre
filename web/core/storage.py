from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage
import boto3
from botocore.exceptions import NoCredentialsError
from urllib.request import urlopen



class StaticStorage(S3Boto3Storage):
    location = 'static'
    default_acl = 'public-read'


class MediaStorage(S3Boto3Storage):
    bucket_name = 'parterre'
    location = 'media'





session = boto3.session.Session()
client = session.client(
    's3',
    region_name='fra1', 
    endpoint_url=settings.AWS_S3_ENDPOINT_URL,  
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
)


def upload_to_spaces(file_name, file_content):
    """
    Upload a file to Digital Ocean Spaces
    """
    try:
        client.upload_fileobj(
            Fileobj=file_content,
            Bucket=settings.PUBLIC_MEDIA_LOCATION,  
            Key=file_name,
            ExtraArgs={'ACL': 'public-read'}  
        )
        print(f"File uploaded successfully {file_name}")
    except NoCredentialsError:
        print("Credentials not available")
    except Exception as e:
        print(f"Failed to upload file: {e}")