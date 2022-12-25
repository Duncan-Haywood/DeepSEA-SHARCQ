output "ecr_url" {
    value = module.public_ecr.repository_url
}
output "ecr_id" {
    value = module.public_ecr.repository_registry_id
}