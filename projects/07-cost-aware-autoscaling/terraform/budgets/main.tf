# Cost guardrails: a monthly budget with forecast alerts, scoped by the Project tag from project 01.
# Activate "Project" as a cost allocation tag in the Billing console first (it isn't retroactive).
terraform {
  required_version = ">= 1.10"
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" }
  }
}

provider "aws" {
  region = "us-east-1"
}

variable "monthly_limit_usd" {
  type    = number
  default = 50
}

variable "alert_email" {
  type = string
}

resource "aws_budgets_budget" "portfolio" {
  name         = "devops-portfolio"
  budget_type  = "COST"
  limit_amount = tostring(var.monthly_limit_usd)
  limit_unit   = "USD"
  time_unit    = "MONTHLY"

  cost_filter {
    name   = "TagKeyValue"
    values = ["user:Project$devops-portfolio"]
  }

  # Forecast alerts fire BEFORE the money is spent; actual alerts fire after.
  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 80
    threshold_type             = "PERCENTAGE"
    notification_type          = "FORECASTED"
    subscriber_email_addresses = [var.alert_email]
  }

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 100
    threshold_type             = "PERCENTAGE"
    notification_type          = "ACTUAL"
    subscriber_email_addresses = [var.alert_email]
  }
}
