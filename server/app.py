from fastapi import FastAPI, HTTPException
from aiobotocore.session import get_session

app = FastAPI()

# AWS S3 Configuration
AWS_ACCESS_KEY_ID = 'your-access-key'
AWS_SECRET_ACCESS_KEY = 'your-secret-key'
BUCKET_NAME = 'your-bucket-name'

@app.get("/files/{file_name}")
async def read_file(file_name: str):
    session = get_session()
    async with session.create_client('s3', region_name='your-region', aws_secret_access_key=AWS_SECRET_ACCESS_KEY, aws_access_key_id=AWS_ACCESS_KEY_ID) as client:
        try:
            response = await client.get_object(Bucket=BUCKET_NAME, Key=file_name)
            async with response['Body'] as stream:
                content = await stream.read()
            return content
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"File not found: {e}")
