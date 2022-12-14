#!/usr/bin/env python3

import aws_cdk as cdk

from cicd.pipeline import PipelineStack
from cicd.terraform_backend import TerraformBackend


def main():
    app = cdk.App()
    TerraformBackend(app, "TerraformBackend")
    PipelineStack(app, "Pipeline")
    app.synth()


if __name__ == "__main__":
    main()
