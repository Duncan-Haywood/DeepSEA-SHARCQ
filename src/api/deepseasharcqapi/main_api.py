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

def create_api():
    app = FastAPI()

    @app.post('/predict/')
    async def predict(files_zip: UploadFile, body: PredictBody):
        #create folder path and awsUtil obj
        time = str(datetime.now())
        folder_path = f'{body.user}_{time}'
        aws_util = AWSUtil(folder_path)
        aws_util.s3_upload_file(files_zip)
        aws_util.store_user_data(body) #TODO

        return {'results': 'request results in a few minutes after we process your files.'}
    @app.get('/results/')
    async def get_results():
        return NotImplementedError
    return app

def run_server(app: ASGIApplication):
    uvicorn.run(app, port=8000, log_level="info")

def main():
    app = create_api()
    run_server(app)
    

if __name__ == '__main__':
    main()