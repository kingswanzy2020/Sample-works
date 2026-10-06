environment              = "staging"
vpc_cidr                 = "10.10.0.0/16"
single_nat_gateway       = true # cheap; accept the single point of failure in staging
db_instance_class        = "db.t4g.micro"
db_multi_az              = false
db_backup_retention_days = 1
db_deletion_protection   = false
