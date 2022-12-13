variable "env" {
  description = "Depolyment environment"
  default     = "dev"
}

variable "region" {
  description = "AWS region"
  default     = "eu-west-1"
}

variable "env" {
  description = "Deployment environment"
  default     = "dev"
}

variable "repository_branch" {
  description = "Repository branch to connect to"
  default     = "main"
}

variable "repository_owner" {
  description = "GitHub repository owner"
  default     = "stojce"
}

variable "repository_name" {
  description = "GitHub repository name"
  default     = "static-web-example"
}

variable "artifacts_bucket_name" {
  description = "S3 Bucket for storing artifacts"
  default     = "artifacts-bucket"
}