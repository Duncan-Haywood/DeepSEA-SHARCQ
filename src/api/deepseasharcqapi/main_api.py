from fastapi import FastAPI, UploadFile
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from mangum import Mangum
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
    async def predict(files: List[UploadFile], body: PredictBody):
        #create folder path and awsUtil obj
        time = str(datetime.now())
        folder_path = f'{body.user}_{time}'
        aws_util = AWSUtil(folder_path)
        #upload to s3 - TODO might need more parallelization or memory management ie in parts for upload - might need some errror handling for uploads greater than ~7 GB (~175 files) (10 gb max on lambda)
        aws_util.s3_upload_files(files)
        #run ai application and close it when done
        aws_util.exec_predict_ecs(email=body.email)

        return {'results': 'we will email you with a signed url to the  predictions at the email you provided. You can download the result files with this.'} # maybe they need to do a get request at this fast api server when they have the url. TODO

    return app

def run_server(app: ASGIApplication):
    uvicorn.run(app, port=5000, log_level="info")

def main():
    app = create_api()
    run_server(app)
    

if __name__ == '__main__':
    main()