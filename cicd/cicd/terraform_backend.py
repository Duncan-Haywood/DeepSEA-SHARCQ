from aws_cdk import Stack
from constructs import Construct
from aws_cdk import aws_dynamodb as dynamodb
from aws_cdk import aws_s3 as s3


class TerraformBackend(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        dynamodb.Table(
            self,
            "TerraformTable",
            name="terraform-lock-table",
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            partition_key=dynamodb.Attribute(
                name="LockID", type=dynamodb.AttributeType.STRING
            ),
        )
        s3.Bucket(
            self,
            "TerraformBucket",
            name="terraform-lock-bucket",
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            versioned=True,
            encryption=s3.BucketEncryption.KMS,
        )
