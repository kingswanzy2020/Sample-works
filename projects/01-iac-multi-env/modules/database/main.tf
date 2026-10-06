terraform {
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" }
  }
}

resource "aws_db_subnet_group" "this" {
  name       = "${var.name}-db"
  subnet_ids = var.subnet_ids
  tags       = var.tags
}

resource "aws_security_group" "db" {
  name        = "${var.name}-db"
  description = "Postgres access from inside the VPC only"
  vpc_id      = var.vpc_id
  tags        = var.tags
}

# This rule is a good drift-detection target: widen it in the console and
# see whether your nightly job notices (docs/break-it.md, experiment 1).
resource "aws_vpc_security_group_ingress_rule" "postgres" {
  security_group_id = aws_security_group.db.id
  cidr_ipv4         = var.allowed_cidr
  from_port         = 5432
  to_port           = 5432
  ip_protocol       = "tcp"
}

resource "aws_db_instance" "this" {
  identifier     = "${var.name}-postgres"
  engine         = "postgres"
  engine_version = "16"
  instance_class = var.instance_class

  allocated_storage     = var.allocated_storage
  max_allocated_storage = var.allocated_storage * 2
  storage_encrypted     = true

  db_name  = "app"
  username = "app"
  # Lets RDS generate and store the password in Secrets Manager, so it never
  # appears in Terraform state. Project 05 builds on this.
  manage_master_user_password = true

  db_subnet_group_name   = aws_db_subnet_group.this.name
  vpc_security_group_ids = [aws_security_group.db.id]
  publicly_accessible    = false

  multi_az                = var.multi_az
  backup_retention_period = var.backup_retention_days
  deletion_protection     = var.deletion_protection
  skip_final_snapshot     = !var.deletion_protection

  tags = var.tags
}
