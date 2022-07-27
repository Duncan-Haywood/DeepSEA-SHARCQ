from aws_cdk import App
from infrastructure.fastapi_stack import FastAPIStack
from infrastructure.unzip_app_stack import UnzipAppStack
from infrastructure.ai_stack import AIStack

def main():
    app = App()

    fastapi = FastAPIStack(app, "FastAPIStack")
    unzipapp = UnzipAppStack(app, "UnzipAppStack", zipped_queue=fastapi.zipped_queue)
    ai = AIStack(app, "AIStack", unzipped_queue=unzipapp.unzipped_queue)
    app.synth()

if __name__ == '__main__':
    main()