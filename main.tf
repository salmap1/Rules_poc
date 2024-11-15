terraform {
  required_providers {
    panos = {
      source  = "PaloAltoNetworks/panos"
      version = "1.9.0"
    }
  }
}

provider "panos" {
  hostname = var.palo_alto_hostname
  username = var.palo_alto_username
  password = var.palo_alto_password
}

variable "palo_alto_hostname" {}
variable "palo_alto_username" {}
variable "palo_alto_password" {}

variable "changes" {
  type        = string
  description = "JSON string containing detected changes for firewall rules."
}

locals {
  parsed_changes = jsondecode(var.changes)
}

resource "panos_security_policy" "security_rules" {
  for_each = tomap(local.parsed_changes["security_rules.json"]["modified_data"])

  rule_name     = each.value["name"]
  source        = each.value["source"]
  destination   = each.value["destination"]
  application   = ["any"]
  action        = each.value["action"]
  description   = "Managed by automation"
  source_zone   = ["any"]
  destination_zone = ["any"]
}

