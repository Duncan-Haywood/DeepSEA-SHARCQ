from aws_cdk import Stack
from constructs import Construct

import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_ecs as ecs
import aws_cdk.aws_ecs_patterns as ecs_patterns
import aws_cdk.aws_s3 as s3
import aws_cdk.aws_sqs as sqs
import aws_cdk.aws_s3_notifications as s3n
import aws_cdk.aws_rds as rds

from os import path


class FastAPIStack(Stack):
    """Creates necessary resources for Rest API functioning.

    Creates a ecs fargate application loadbalance service which runs the docker image for fast api from self.image_path attribute, attaches s3 and sqs for outputs from this. TODO: Creates a RDS for storage of user data for recall."""

    def __init__(
        self,
        scope: Construct,
        id: str,
        **kwargs,
    ) -> None:
        super().__init__(scope, id, **kwargs)
        self.image_path = path.join(path.dirname(__file__), "..", "..", "api")

        # Create VPC
        self.vpc = ec2.Vpc(self, "MyVPC", max_azs=3)

        # # create database
        # self.db = rds.DatabaseInstance(self, "Database",
        # engine=rds.DatabaseInstanceEngine.postgres(),
        # instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.SMALL),
        # vpc = self.vpc,
        # )

        # zipped files bucket
        self.s3_output_bucket = s3.Bucket(self, "ZippedBucket")

        # AI results bucket
        self.s3_results_bucket = s3.Bucket(self, "AIResultsBucket")

        # SQS output queue from bucket which listens to object creations in zipped bucket
        self.zipped_queue = sqs.Queue(self, "ZipsQueue")
        self.s3_output_bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED, s3n.SqsDestination(self.zipped_queue)
        )

        # get resource names as environment for use in service TODO production/etc
        self.environment = dict(
            ZIPPED_BUCKET_NAME=self.s3_output_bucket.bucket_name,
            AI_RESULTS_BUCKET_NAME=self.s3_results_bucket.bucket_name,
        )

        # Create Fargate Service and ALB
        # Create ecs Cluster
        self.ecs_cluster = ecs.Cluster(
            self,
            "MyECSCluster",
            vpc=self.vpc,
        )
        # docker image from dockerFile plus environment passed to it
        image = ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
            image=ecs.AssetImage(self.image_path), environment=self.environment
        )
        # load balanced service
        self.ecs_service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self,
            "FastAPIService",
            cluster=self.ecs_cluster,
            cpu=4096,
            memory_limit_mib=8192,
            desired_count=0,
            task_image_options=image,
        )
        # autoscaling setup
        self.scalable_target = self.ecs_service.service.auto_scale_task_count(
            min_capacity=0, max_capacity=2
        )
        # autoscaling based
        self.scalable_target.scale_on_request_count(
            "RequestScaling",
            requests_per_target=1,
            scale_in_cooldown=0,
            scale_out_cooldown=60,
        )
