terraform {
  required_providers {
    panos = {
      source  = "PaloAltoNetworks/panos"
      version = "1.9.0"
    }
  }
}

provider "panos" {
  hostname = var.paloalto_hostname
  username = var.paloalto_username
  password = var.paloalto_password
}

variable "paloalto_hostname" {
  type        = string
  description = "The hostname or IP address of the Palo Alto firewall"
}

variable "paloalto_username" {
  type        = string
  description = "The username for the Palo Alto firewall"
}

variable "paloalto_password" {
  type        = string
  description = "The password for the Palo Alto firewall"
  sensitive   = true
}


# Output the raw content of the file for debugging
output "raw_json_content" {
  value = file("${path.module}/security_rules.json")
}
 
# Try to decode the JSON
locals {
  rules = jsondecode(file("${path.module}/security_rules.json"))
}
 
# Output the decoded rules
output "decoded_rules" {
  value = local.rules
}
