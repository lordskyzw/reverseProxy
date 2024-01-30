from fastapi import FastAPI, HTTPException
from aiobotocore.session import get_session

app = FastAPI()

# AWS S3 Configuration
AWS_ACCESS_KEY_ID = 'AKIATCKAQNC5OYCUN2N6'
AWS_SECRET_ACCESS_KEY = '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'
BUCKET_NAME = 'chumbucketzw'

@app.get("/files/{file_name}")
async def read_file(file_name: str):
    session = get_session()
    async with session.create_client('s3', region_name='us-east-1', aws_secret_access_key=AWS_SECRET_ACCESS_KEY, aws_access_key_id=AWS_ACCESS_KEY_ID) as client:
        try:
            response = await client.get_object(Bucket=BUCKET_NAME, Key=file_name)
            async with response['Body'] as stream:
                content = await stream.read()
            return content
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"File not found: {e}")
