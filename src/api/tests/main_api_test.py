from deepseasharcqapi import main_api
from fastapi import FastAPI

def test_main():
    main_api.main()
    #TODO check results
    #TODO close server

def test_create_api():
    main_api.create_api()
    #TODO check results

def test_run_server():
    app = FastAPI()
    main_api.run_server(app)
    #TODO check results and close server