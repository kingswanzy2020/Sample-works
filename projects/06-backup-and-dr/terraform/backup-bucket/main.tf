# Backup bucket designed to survive: accidental deletes (versioning), ransomware or a
# compromised admin (object lock), and a regional outage (replication: a milestone).
# DECISION (ADR-0004): ideally this lives in a SEPARATE AWS account from production.
terraform {
  required_version = ">= 1.10"
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" }
  }
}

provider "aws" {
  region = var.region
}

variable "region" {
  type    = string
  default = "us-west-2" # a different region from production (us-east-1 in project 01)
}

variable "bucket_name" {
  type = string
}

variable "retention_days" {
  type    = number
  default = 30
}

resource "aws_s3_bucket" "backups" {
  bucket              = var.bucket_name
  object_lock_enabled = true # can only be set at creation
}

resource "aws_s3_bucket_versioning" "backups" {
  bucket = aws_s3_bucket.backups.id
  versioning_configuration {
    status = "Enabled"
  }
}

# GOVERNANCE mode: users with s3:BypassGovernanceRetention can still delete (good for labs).
# COMPLIANCE mode: NOBODY can delete before expiry, not even root. Choose deliberately.
resource "aws_s3_bucket_object_lock_configuration" "backups" {
  bucket = aws_s3_bucket.backups.id
  rule {
    default_retention {
      mode = "GOVERNANCE"
      days = var.retention_days
    }
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "backups" {
  bucket = aws_s3_bucket.backups.id
  rule {
    id     = "tiering"
    status = "Enabled"
    filter {}
    transition {
      days          = 7
      storage_class = "STANDARD_IA"
    }
    noncurrent_version_expiration {
      noncurrent_days = var.retention_days + 7
    }
  }
}

resource "aws_s3_bucket_public_access_block" "backups" {
  bucket                  = aws_s3_bucket.backups.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# The writer can put objects but NOT delete them. A compromised backup job can't wipe history.
data "aws_iam_policy_document" "writer" {
  statement {
    actions   = ["s3:PutObject", "s3:ListBucket", "s3:GetObject"]
    resources = [aws_s3_bucket.backups.arn, "${aws_s3_bucket.backups.arn}/*"]
  }
}

resource "aws_iam_policy" "backup_writer" {
  name   = "${var.bucket_name}-writer"
  policy = data.aws_iam_policy_document.writer.json
}

output "bucket" {
  value = aws_s3_bucket.backups.bucket
}

output "writer_policy_arn" {
  value = aws_iam_policy.backup_writer.arn
}
