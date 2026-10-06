output "vpc_id" {
  value = module.network.vpc_id
}

output "private_subnet_ids" {
  value = module.network.private_subnet_ids
}

output "db_endpoint" {
  value = module.database.endpoint
}

output "db_secret_arn" {
  value = module.database.master_user_secret_arn
}
