import base64
import uuid
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
        new_filename = create_new_filename(file_name)
        response = s3_client.upload_fileobj(image, bucket, new_filename)
        
        url = '{}/{}/{}'.format(s3_client.meta.endpoint_url, bucket, new_filename)
        return url

    except ClientError as e:
        logging.error(e)

def create_new_filename(file_name):
    file_name_split = file_name.rsplit('.', 1)
    return str(uuid.uuid4()) + '_' + file_name_split[0] + ".png"        