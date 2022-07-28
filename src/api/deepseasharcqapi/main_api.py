from fastapi import FastAPI, UploadFile
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from .aws_util import AWSUtil
import uvicorn
from asgiref.typing import ASGIApplication
import boto3
import logging

logger = logging.getLogger(__name__)

class Body(BaseModel):
    user_name: str
    api_key: str

def generate_presigned_url(s3_client, client_method, method_parameters, expires_in):
    """
    Generate a presigned Amazon S3 URL that can be used to perform an action.

    :param s3_client: A Boto3 Amazon S3 client.
    :param client_method: The name of the client method that the URL performs.
    :param method_parameters: The parameters of the specified client method.
    :param expires_in: The number of seconds the presigned URL is valid for.
    :return: The presigned URL.
    """
    try:
        url = s3_client.generate_presigned_url(
            ClientMethod=client_method,
            Params=method_parameters,
            ExpiresIn=expires_in
        )
        logger.info("Got presigned URL: %s", url)
    except ClientError:
        logger.exception(
            "Couldn't get a presigned URL for client method '%s'.", client_method)
        raise
    return url
class API: 
    def __init__(self):
        self.app = FastAPI() # type: ASGIApplication
        self.folder_path=None
        self.aws_util = None
        self.s3_client = boto3.client("s3")
        self.expires_in = 1800 # 30 minutes
    
    def create_api(self):
        """two paths: post: predict and get: results"""

        @self.app.post('/upload_url/')
        async def get_upload_signed_url(Body):
            generate_presigned_url(self.s3_client, "put", method_parameters, self.expires_in)

        @self.app.post('/download_url/')
        async def get_download_signed_url(Body):
            return NotImplementedError
    
    def run_server(self):
        uvicorn.run(self.app, port=8000, log_level="info")
        
    def main(self):
        self.create_api()
        self.run_server()

def main():
    API().main()
    

if __name__ == '__main__':
    main()