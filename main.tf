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

locals {
  rules = jsondecode(file("${path.module}/security_rules.json"))
}

resource "panos_security_rule" "firewall_rules" {
  for_each = local.rules

  name                  = each.value["name"]
  description           = each.value["description"]
  source_zones          = each.value["source_zones"]
  source_addresses      = each.value["source_addresses"]
  source_users          = each.value["source_users"]
  destination_zones     = each.value["destination_zones"]
  destination_addresses = each.value["destination_addresses"]
  categories            = each.value["categories"]
  applications          = each.value["applications"]
  services              = each.value["services"]
  action                = each.value["action"]
  tags                  = each.value["tags"]
}


