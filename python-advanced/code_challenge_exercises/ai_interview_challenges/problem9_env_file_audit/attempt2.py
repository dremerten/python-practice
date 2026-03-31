import json



def audit_env_file(file_path: str) -> dict:
    results = {
        "total_variables": 0,
        "emtpy_values": [],
        "duplicate_variables": [],
        "sensitive_variables": []
    }
    seen_variables = set()
    duplicates = set()
    sensitive_keywords = {"PASSWORD", "SECRET", "KEY", "TOKEN"}

    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                if "=" not in line:
                    continue

                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()
                if not key:
                    continue

                results["total_variables"] += 1
                if not value:
                    results["emtpy_values"].append(key)
                
                if key in seen_variables:
                    duplicates.add(key)    
                else:
                    seen_variables.add(key)

                upper_key = key.upper()
                if any(keyword in upper_key for keyword in sensitive_keywords):
                    results["sensitive_variables"].append(key)

            results["duplicate_variables"] = sorted(duplicates)
            results["emtpy_values"].sort()
            results["sensitive_variables"].sort()

        return results

    except FileNotFoundError:
        print(
            f"The file at {file_path} can be found or does not exist"
            )
        return results
    except Exception as error:
        print(
            f"An unknown error occured: {error}"
            )

if __name__ == "__main__":
    result = audit_env_file(file_path=".env")
    print(json.dumps(result, indent=4))