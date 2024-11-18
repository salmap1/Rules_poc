terraform {
  required_providers {
    panos = {
      source  = "PaloAltoNetworks/panos"
      version = "1.9.0"
    }
  }
}

# Configure the provider
provider "panos" {
  hostname = var.hostname
  username = var.username
  password = var.password 
}

# Load the security rules from the JSON file
locals {
  rules = jsondecode(file("${path.module}/security_rules.json"))
}

# Define the security policy for Palo Alto
resource "panos_security_policy" "firewall_rules" {
  # Create the rule block dynamically from the local rules
  dynamic "rule" {
    for_each = local.rules  # Iterate over the rules loaded from the JSON file
    content {
      name                   = rule.value["name"]
      description            = rule.value["description"]
      source_zones           = rule.value["source_zones"]
      source_addresses       = rule.value["source_addresses"]
      source_users           = rule.value["source_users"]
      destination_zones      = rule.value["destination_zones"]
      destination_addresses  = rule.value["destination_addresses"]
      categories             = rule.value["categories"]
      applications           = rule.value["applications"]
      services               = rule.value["services"]
      action                 = rule.value["action"]
      tags                   = rule.value["tags"]
    }
  }
}

