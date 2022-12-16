terraform {
  cloud {
    organization = "automate-ai"
    hostname = "app.terraform.io"
    workspaces {
      tags =["deepsea-sharcq-packing"]
    }
  }
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 3.20.0"
    }

    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = ">= 2.0.1"
    }
  }
}
