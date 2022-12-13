data "template_file" "buildspec" {
  template = "${file("buildspec.yml")}"
  vars = {
    env          = var.env
  }
}

resource "aws_codebuild_project" "terraform_apply" {
  name           = "cicd"
  service_role   = aws_iam_role.codebuild_role.arn
  tags = {
    Environment = var.env
  }

  artifacts {
    type                   = "NONE"
  }

  environment {
    compute_type                = "BUILD_GENERAL1_LARGE"
    image                       = "aws/codebuild/amazonlinux2-x86_64-standard:4.0"
    image_pull_credentials_type = "CODEBUILD"
    privileged_mode             = true
    type                        = "LINUX_CONTAINER"
  }

  cache {
    type = "LOCAL"
    modes = "LOCAL_DOCKER_LAYER_CACHE"
  }

  source {
    buildspec           = data.template_file.buildspec.rendered
    type                = "CODEPIPELINE"
  }
}