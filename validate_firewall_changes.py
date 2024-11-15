import json
import sys
import os


def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)


def detect_changes(old_data, new_data):
    old_keys = set(old_data.keys())
    new_keys = set(new_data.keys())

    added = new_keys - old_keys
    deleted = old_keys - new_keys
    modified = {key for key in old_keys & new_keys if old_data[key] != new_data[key]}

    return {
        "added": list(added),
        "deleted": list(deleted),
        "modified": list(modified),
        "added_data": {key: new_data[key] for key in added},
        "modified_data": {key: new_data[key] for key in modified},
    }


def validate_changes(file):
    old_file = f"old_{file}"
    new_file = f"new_{file}"

    if os.path.exists(old_file) and os.path.exists(new_file):
        old_data = load_json(old_file)
        new_data = load_json(new_file)
        changes = detect_changes(old_data, new_data)

        errors = []
        for added_rule in changes["added"]:
            rule = new_data[added_rule]
            required_fields = ["name", "source", "destination", "action"]
            for field in required_fields:
                if field not in rule:
                    errors.append(f"Missing required field '{field}' in added rule '{added_rule}'.")

        if errors:
            print("Validation Errors:")
            for error in errors:
                print(f" - {error}")
            sys.exit(1)

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
            all_changes[file] = changes

    with open("detected_changes.json", "w") as outfile:
        json.dump(all_changes, outfile)

