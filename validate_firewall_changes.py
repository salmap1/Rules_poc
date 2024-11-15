import json
import sys
import os

def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def detect_changes(old_data, new_data):
    # Detect added, modified, and deleted keys
    old_keys = set(old_data.keys())
    new_keys = set(new_data.keys())

    added = new_keys - old_keys
    deleted = old_keys - new_keys
    modified = {key for key in old_keys & new_keys if old_data[key] != new_data[key]}

    return {
        "added": list(added),
        "deleted": list(deleted),
        "modified": list(modified),
        "added_data": {key:new_data[key] for key in added},
        "modified_data": {key:new_data[key] for key in modified}
    }

def validate_changes(file):
    old_file = f"old_{file}"
    new_file = f"new_{file}"

    if os.path.exists(old_file) and os.path.exists(new_file):
        old_data = load_json(old_file)
        new_data = load_json(new_file)
        changes = detect_changes(old_data, new_data)
        
        print(f"Changes in {file}:")
        print(json.dumps(changes, indent=2))

        # Validate each type of change based on rules
        errors = []
        
        # Example validation: if a new rule is added, check for required fields
        for added_rule in changes["added"]:
            if "name" not in new_data[added_rule]:
                errors.append(f"New rule '{added_rule}' is missing 'name'")

        for deleted_rule in changes["deleted"]:
            print(f"Rule '{deleted_rule}' will be deleted")

        # Example validation: check modified rules for proper format
        for modified_rule in changes["modified"]:
            # if not new_data[modified_rule].get("field").startswith("prefix_"):
                # errors.append(f"Modified rule '{modified_rule}' has incorrect format in 'field'")

            # print(new_data[modified_rule].keys())
            if not new_data[modified_rule].get("name").startswith("SRE"):
                    errors.append(f"Modified rule '{modified_rule}' has incorrect format in 'name'")
            
        if errors:
            print("Validation Errors:")
            for error in errors:
                print(f" - {error}")
            sys.exit(1)  # Exit with error status if validation fails

        return changes

    else:
        print(f"Could not find both versions of {file} for comparison.")
        return {}

if __name__ == "__main__":
    changed_files = sys.argv[1:]
    all_changes = {}

    for file in changed_files:
        changes = validate_changes(file)
        if changes:
            print(f"{'*'*20}\nchanges detected\n{'*'*20}")
            all_changes[file] = changes

    print(f"{'*'*20}\nall_changes:{all_changes}\n{'*'*20}")

    # Save the changes to a JSON file for Terraform to read
    with open("detected_changes.json", "w") as outfile:
        json.dump(all_changes, outfile)

    
    # debug step
    # Open and read the JSON file
    with open('detected_changes.json', 'r') as file:
        data = json.load(file)

    # Print the data
    print(data)
