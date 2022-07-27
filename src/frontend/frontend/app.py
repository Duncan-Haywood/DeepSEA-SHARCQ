from dash import Dash
import dash_auth

from flask import Flask
from dash_cognito_auth import CognitoOAuth

def main():
    server = Flask(__name__)
    app = Dash(__name__, server=server, url_base_pathname='/')
    auth = CognitoOAuth(app)
    

if __name__=='__main__':
    main()
