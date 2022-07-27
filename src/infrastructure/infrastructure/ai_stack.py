from aws_cdk import Stack
from constructs import Construct
import aws_cdk.aws_lambda as lambda_
import aws_cdk.aws_lambda_event_sources as eventsources
import aws_cdk.aws_s3 as s3
import aws_cdk.aws_sqs as sqs
import aws_cdk.aws_s3_notifications as s3n
from os import path
class AIStack(Stack):
    def __init__(
        self,
        scope: Construct,
        id: str,
        prod: bool = False,
        unzipped_queue = None,
        **kwargs,
    ) -> None:
        super().__init__(scope, id, **kwargs)

        # path to dockerfile
        self.file_path = path.join(path.dirname(__file__), "..", "..", "ai")

        # unzipped input queue
        self.unzipped_queue = unzipped_queue

        # output s3 bucket 
        self.unzipped_results_s3  = s3.Bucket(self, "UnzippedResultsBucket")
        
        # output queue
        self.sqs_results_unzipped = sqs.Queue(self, "UnzippedResultsQueue")

        # add event listener from s3 to sqs
        self.unzipped_results_s3.add_event_notification(s3.EventType.OBJECT_CREATED, s3n.SqsDestination(self.sqs_results_unzipped))

        # environment for lambda function
        self.environment = dict(UNZIPPED_QUEUE_NAME=self.unzipped_queue.queue_name, UNZIPPED_RESULTS_BUCKET_NAME=self.unzipped_results_s3.bucket_name)


        # lambda from dockerfile:
        self.fn = lambda_.DockerImageFunction(self, "AIFunction",
            code=lambda_.DockerImageCode.from_image_asset(self.file_path), 
            environment = self.environment
        )

        # add lambda listener to unzipped sqs
        self.fn.add_event_source(eventsources.SqsEventSource(self.unzipped_queue))
