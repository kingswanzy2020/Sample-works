provider "aws" {
  region = var.region
  default_tags {
    tags = local.tags
  }
}

locals {
  name = "sample-${var.environment}"
  tags = {
    Project     = "devops-portfolio"
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

module "network" {
  source             = "../../modules/network"
  name               = local.name
  cidr_block         = var.vpc_cidr
  single_nat_gateway = var.single_nat_gateway
  tags               = local.tags
}

module "database" {
  source                = "../../modules/database"
  name                  = local.name
  vpc_id                = module.network.vpc_id
  subnet_ids            = module.network.private_subnet_ids
  allowed_cidr          = module.network.vpc_cidr
  instance_class        = var.db_instance_class
  multi_az              = var.db_multi_az
  backup_retention_days = var.db_backup_retention_days
  deletion_protection   = var.db_deletion_protection
  tags                  = local.tags
}
