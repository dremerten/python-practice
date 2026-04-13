import json


SENSITIVE_PORTS = {22, 3389, 5432, 3306, 6379}

REQUIRED_KEYS = {
    "rule_id",
    "environment",
    "protocol",
    "port",
    "source",
    "description",
    "enabled"
}



def validate_rule(rule: dict) -> list[str]:
    problems = []

    if not isinstance(rule, dict):
        return ["Invalid rule: not a dictionary"]

    

    return problems







def audit_firewall(rules: list[dict]) -> dict:
    results = {}


    breakpoint()

    return results







if __name__ == "__main__":
    FILE_PATH = "firewall_rules.json"
    
    try:
        with open(FILE_PATH, 'r') as f:
            rules = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(
            f"The {FILE_PATH} file cannot be found or does not exist!"
        )
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        rules = []  # prevent crash
    
    # Debugging
    for rule in rules:
        validate_rule(rule)

audit_firewall(rules)