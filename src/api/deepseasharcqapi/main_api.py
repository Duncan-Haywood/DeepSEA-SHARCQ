from fastapi import FastAPI, UploadFile
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from .aws_util import AWSUtil
import uvicorn
from asgiref.typing import ASGIApplication


class PredictBody(BaseModel):
    user: str
    email: str
    api_key: Optional[str]

class API: 
    def __init__(self):
        self.app = FastAPI() # type: ASGIApplication
        self.time = str(datetime.now())
        self.folder_path=None
        self.aws_util = None
    def create_api(self):
        """two paths: post: predict and get: results"""
        @self.app.post('/predict/')
        async def predict(files_zip: UploadFile, body: PredictBody):
            #create folder path and awsUtil obj
            self.folder_path = f'{body.user}_{self.time}'
            self.aws_util = AWSUtil(self.folder_path)

            self.aws_util.s3_upload_file(files_zip)
            self.aws_util.store_user_data(body) #TODO

            return {'results': 'request results in a few minutes after we process your files.'}

        @self.app.get('/results/')
        async def get_results():
            file = self.aws_util.s3_download_file(self.folder_path)
            return dict(results=file)

    def run_server(self):
        uvicorn.run(self.app, port=8000, log_level="info")
        
    def main(self):
        self.create_api()
        self.run_server()

def main():
    API().main()
    

if __name__ == '__main__':
    main()