variable "name" {
  type = string
}

variable "cidr_block" {
  type = string
}

variable "az_count" {
  type    = number
  default = 2
}

variable "single_nat_gateway" {
  type        = bool
  default     = true
  description = "true = one shared NAT (cheap, single point of failure); false = one per AZ"
}

variable "tags" {
  type    = map(string)
  default = {}
}
