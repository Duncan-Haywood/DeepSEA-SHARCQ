from fastapi import FastAPI
from pydantic import BaseModel
from wildroot_aws_util.aws_util import AWSUtil
import uvicorn
from asgiref.typing import ASGIApplication
import os
import mangum


class Body(BaseModel):
    user_name: str
    api_key: str


class API:
    def __init__(self):
        self.app = FastAPI()  # type: ASGIApplication
        self.folder_path = None
        self.aws_util = None
        self.expires_in = 1800  # 30 minutes
        self.aws_util = AWSUtil()
        self.create_api()


    def create_api(self):
        """two paths: post: predict and get: results"""

        @self.app.post("/upload_url/")
        async def get_upload_signed_url(Body):
            method_parameters = dict(
                Bucket=os.get_environ("ZIPPED_BUCKET"), Key=None
            )  # TODO decide on key for files
            url = self.aws_util.generate_presigned_url(
                "put", method_parameters, self.expires_in
            )
            return dict(upload_url=url)

        @self.app.post("/download_url/")
        async def get_download_signed_url(Body):
            method_parameters = dict(
                Bucket=os.get_environ("ZIPPED_RESULTS_BUCKET"), Key=None
            )  # TODO decide on key for files
            url = self.aws_util.generate_presigned_url(
                "get", method_parameters, self.expires_in
            )
            return dict(download_url=url)
        return self.app
    def run_server(self):
        uvicorn.run(self.app, port=8000, log_level="info")


if __name__ == "__main__":
    API().run_server()
