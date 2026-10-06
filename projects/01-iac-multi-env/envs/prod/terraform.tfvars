environment              = "prod"
vpc_cidr                 = "10.20.0.0/16"
single_nat_gateway       = false # one NAT per AZ: document the cost of this in ADR-0001 / scale.md
db_instance_class        = "db.t4g.small"
db_multi_az              = true
db_backup_retention_days = 7
db_deletion_protection   = true
