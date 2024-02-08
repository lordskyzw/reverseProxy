from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from botocore.exceptions import ClientError
from aiobotocore.session import get_session
import logging
import os

logging.basicConfig(level=logging.INFO)

app = FastAPI()

# AWS S3 Configuration
aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
BUCKET_NAME = 'chumbucketzw'

# Initialize S3 client outside the request handler
session = get_session()
client = session.create_client('s3', region_name='us-east-1',
                               aws_secret_access_key=aws_secret_access_key,
                               aws_access_key_id=aws_access_key_id)
@app.get("/files/{file_name}")
async def read_file(file_name: str):
    logging.info("Fetching file %s", file_name)
    path = f"example/{file_name}"
    try:
        response = client.get_object(Bucket=BUCKET_NAME, Key=path)
        content = response['Body'].read()

        headers = {"Content-Disposition": f"attachment; filename={file_name}"}
        logging.info("File %s fetched successfully", file_name)
        
        return Response(content=content, media_type="application/octet-stream", headers=headers)
        
    except ClientError as e:
        logging.error("Error: %s", e)
        raise HTTPException(status_code=404, detail=f"File not found: {e}")

