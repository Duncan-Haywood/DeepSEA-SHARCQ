module "public_ecr" {
  source = "terraform-aws-modules/ecr/aws"

  repository_name = "deepsea-sharcq-api"
  repository_type = "public"

  public_repository_catalog_data = {
    description       = "Fast API for deepsea-sharcq"
    operating_systems = ["Linux"]
    architectures     = ["x86"]
  }

  tags = {
    Terraform   = "true"
    Environment = "prod"
  }
}