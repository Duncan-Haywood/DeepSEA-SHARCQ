from aws_cdk import Stack
from constructs import Construct
import aws_cdk.aws_lambda as lambda_
import aws_cdk.aws_lambda_event_sources as eventsources
import aws_cdk.aws_s3 as s3
import aws_cdk.aws_sqs as sqs
import aws_cdk.aws_s3_notifications as s3n


from os import path


class UnzipAppStack(Stack):
    """Creates the necessary resources for the lambda unzip  microservice.

    Creates lambda function from dockerfile specified at self.file_path. Creates a s3 bucket and sqs queue for unzipped files output. Lambda function has trigger from input queue."""

    def __init__(
        self,
        scope: Construct,
        id: str,
        prod: bool = False,
        zipped_queue=None,
        **kwargs,
    ) -> None:
        super().__init__(scope, id, **kwargs)

        # file path to dockerfile
        self.file_path = path.join(path.dirname(__file__), "..", "..", "unzip_app")

        # input queue for files to unzip
        self.zipped_queue = zipped_queue

        # output bucket for unzipped files
        self.unzipped_s3 = s3.Bucket(self, "UnzippedBucket")

        # SQS output queue from bucket which listens to object creations in unzippede bucket
        self.unzipped_queue = sqs.Queue(self, "UnzippedQueue")
        self.unzipped_s3.add_event_notification(
            s3.EventType.OBJECT_CREATED, s3n.SqsDestination(self.sqs_unzipped)
        )

        # environment for lambda function
        self.environment = dict(
            ZIPPED_QUEUE_NAME=self.zipped_queue.queue_name,
            UNZIPPED_BUCKET_NAME=self.unzipped_s3.bucket_name,
        )

        # lambda function from docker image
        self.fn = lambda_.DockerImageFunction(
            self,
            "UnZipFunction",
            code=lambda_.DockerImageCode.from_image_asset(self.file_path),
            environment=self.environment,
        )

        # queue trigger for lambda function
        self.fn.add_event_source(eventsources.SqsEventSource(self.zipped_queue))
