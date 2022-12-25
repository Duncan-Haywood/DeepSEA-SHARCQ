from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from deepseasharcq.main import DeepSeaSharcq



app = FastAPI()  # type: ASGIApplication

@app.post("/predict/")
async def predict(data):
    dss = DeepSeaSharcq()
    response = dss.predict(data)
    return response
@app.get("/")
async def main():
    return "server working on deepseasharcq; see /docs for usage of api"
def run_server():
    uvicorn.run(app, port=8000, log_level="info")




if __name__ == "__main__":
    run_server()
