import json


def audit_env_file(file_path: str) -> dict:
    results = {
        "total_variables": 0,
        "empty_values": [],
        "duplicate_variables": [],
        "sensitive_variables": []
    }

    # Helpers
    seen_variables = set()
    duplicates = set()
    sensitive_keywords = ["PASSWORD", "SECRET", "KEY", "TOKEN"]

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                if "=" not in line:
                    continue

                key, value = line.strip().split("=")
                if not key:
                    continue

                results["total_variables"] += 1

                if not value:
                    results["empty_values"].append(key)

                if key in seen_variables:
                    duplicates.add(key)
                else:
                    seen_variables.add(key)

                if any(keyword in key.upper() for keyword in sensitive_keywords):
                    results["sensitive_variables"].append(key)
                
    except FileNotFoundError as err:
        print(f"The file {file_path} can't be found or does not exits: {err}")
        return results
    except Exception as err:
        print(f"An unknown error occured: {err}")
        return results

    results["duplicate_variables"] = sorted(duplicates)
    results["empty_values"].sort()
    results["sensitive_variables"].sort()

    return results

result = audit_env_file(".env")
print(json.dumps(result, indent=4))