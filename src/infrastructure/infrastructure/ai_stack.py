from aws_cdk import Stack
from constructs import Construct

class AIStack(Stack):
    def __init__(
        self,
        scope: Construct,
        id: str,
        prod: bool = False,
        unzipped_queue = None,
        results_s3_bucket = None,
        **kwargs,
    ) -> None:
        super().__init__(scope, id, **kwargs)

        # path to dockerfile
        self.file_path = path.join(path.dirname(__file__), "..", "..", "ai")

        # lambda from dockerfile:

        # add lambda listener to unzipped sqs

        # output s3 bucket - from fastapi stack.

        