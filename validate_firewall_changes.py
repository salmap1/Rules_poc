import json
import sys
import os

def load_json(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    if os.path.getsize(file_path) == 0:
        raise ValueError(f"File is empty: {file_path}")
    with open(file_path, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in file {file_path}: {e}")

def validate_changes(file_path):
    data = load_json(file_path)
    for rule_name, rule in data.items():
        if "name" not in rule or not rule["name"]:
            raise ValueError(f"Rule {rule_name} is missing a 'name'.")
        if "source_addresses" not in rule or not isinstance(rule["source_addresses"], list):
            raise ValueError(f"Rule {rule_name} has invalid 'source_addresses'.")
        if "destination_addresses" not in rule or not isinstance(rule["destination_addresses"], list):
            raise ValueError(f"Rule {rule_name} has invalid 'destination_addresses'.")
        if "action" not in rule or rule["action"] not in ["allow", "deny"]:
            raise ValueError(f"Rule {rule_name} has an invalid 'action'.")
        print(f"Rule {rule_name} passed validation.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_firewall_changes.py <file>")
        sys.exit(1)
    file_path = sys.argv[1]
    validate_changes(file_path)

