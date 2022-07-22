from aws_cdk import App
from infrastructure.fastapi_stack import FastAPIStack
from infrastructure.unzip_app_stack import UnzipAppStack
from infrastructure.ai_stack import AIStack

def main():
    app = App()

    FastAPIStack(app, "FastAPIStack")
    UnzipAppStack(app, "UnzipAppStack")
    AIStack(app, "AIStack")
    app.synth()

if __name__ == '__main__':
    main()