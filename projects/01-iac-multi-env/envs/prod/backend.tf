terraform {
  backend "s3" {
    bucket       = "REPLACE-ME-tfstate" # output of bootstrap/
    key          = "prod/terraform.tfstate"
    region       = "us-east-1"
    encrypt      = true
    use_lockfile = true # S3-native locking (Terraform >= 1.10), no DynamoDB table needed
  }
}
