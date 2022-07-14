from aws_cdk import Stack
from constructs import Construct

class AIStack(Stack):
    def __init__(
        self,
        scope: Construct,
        id: str,
        prod: bool = False,
        **kwargs,
    ) -> None:
        super().__init__(scope, id, **kwargs)