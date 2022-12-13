from constructs import Construct
from aws_cdk import Stack, pipelines, Stage
from aws_cdk import aws_codebuild as codebuild

OWNER_REPO = "Duncan-Haywood/diffusion-endpoint"
BRANCH = "main"


class PipelineStack(Stack):
    def __init__(
        self, scope: Construct, construct_id: str, branch=BRANCH, **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        source = pipelines.CodePipelineSource.git_hub(OWNER_REPO, branch)
        self.pipeline = pipelines.CodePipeline(
            self,
            "Pipeline",
            synth=pipelines.CodeBuildStep(
                "Synth",
                input=source,
                install_commands=[
                    "npm install -g aws-cdk",
                    "pip install aws-cdk-lib",
                    "cd cicd",
                ],
                commands=[
                    "cdk synth --output ../cdk.out",
                ],
            ),
            docker_enabled_for_self_mutation=True,
            code_build_defaults=pipelines.CodeBuildOptions(
                build_environment=codebuild.BuildEnvironment(
                    compute_type=codebuild.ComputeType.LARGE,
                    # build_image=codebuild.LinuxBuildImage.from_asset(
                    #     self, "GeneralBuildImage", directory=""
                    # ),
                ),
                cache=codebuild.Cache.local(codebuild.LocalCacheMode.DOCKER_LAYER),
            ),
            asset_publishing_code_build_defaults=pipelines.CodeBuildOptions(
                build_environment=codebuild.BuildEnvironment(
                    compute_type=codebuild.ComputeType.LARGE,
                ),
                cache=codebuild.Cache.local(codebuild.LocalCacheMode.DOCKER_LAYER),
            ),
        )
        self.pipeline.add_stage(
            EndpointStage(
                self,
                "TestStage",
                production=False,
            ),
        )
        self.pipeline.add_stage(
            EndpointStage(
                self,
                "ProdStage",
                production=True,
            ),
            pre=[pipelines.ManualApprovalStep("PromoteToProd")],
        )


class EndpointStage(Stage):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        production: bool = False,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
