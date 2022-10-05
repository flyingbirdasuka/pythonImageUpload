import base64
import boto3
import logging
import os
from PIL import Image
from io import BytesIO
from base64 import b64decode
from botocore.exceptions import ClientError

# Boto3 makes it easy to integrate your Python application, library, or script with AWS services including Amazon S3, Amazon EC2, Amazon DynamoDB, and more.
s3_client = boto3.client('s3')  
bucket = os.environ['BUCKET_NAME']

def image_upload(event, context):

    file_name = event['name']
    file_content = Image.open(BytesIO(b64decode(event['image'].split(',')[1])))

    try:
        image = BytesIO() 
        file_content.save(image, format=file_content.format)
        image.seek(0)
        response = s3_client.upload_fileobj(image, bucket, file_name)
        
        url = '{}/{}/{}'.format(s3_client.meta.endpoint_url, bucket, file_name)
        return url

    except ClientError as e:
        logging.error(e)