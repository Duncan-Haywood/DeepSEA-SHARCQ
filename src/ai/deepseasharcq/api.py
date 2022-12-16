from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from deepseasharcq.main import DeepSeaSharcq


class API:
    def __init__(self):
        self.app = FastAPI()  # type: ASGIApplication
        
        @self.app.post("/predict/")
        async def predict(data):
            dss = DeepSeaSharcq()
            response = dss.predict(data)
            return response

    def run_server(self):
        uvicorn.run(self.app, port=8000, log_level="info")


app = API()

if __name__ == "__main__":
    app.run_server()
