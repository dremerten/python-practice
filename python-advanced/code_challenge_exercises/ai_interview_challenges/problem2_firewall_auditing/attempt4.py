import json


SENSITIVE_PORTS = {22, 3389, 5432, 3306, 6379, 443}

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

    rule_id = rule.get("rule_id", "<unknown>")
    missing_keys = REQUIRED_KEYS - rule.keys()
    if missing_keys:
        problems.append(f"Rule: {rule_id} is missing requred keys: {missing_keys}")
        return problems
    
    if rule["enabled"] != True:
        problems.append(f"Rule: {rule_id} is not enabled" )

    protocol = rule.get("protocol")
    if protocol not in ("tcp", "udp"):
        problems.append(f"Rule: {rule_id} protocol not allowed. Got: {protocol}")

    try:
        port = rule.get("port")
        if port < 1 or port > 65535:
            problems.append(f"Rule: {rule_id}'s port value must be between 1 to 65535")
    except TypeError:
        problems.append(f"Rule: {rule_id} port number is invalid, got: {port}")
    
    try:
        if rule["source"] == "0.0.0.0/0":
            if port in SENSITIVE_PORTS:
                problems.append(f"Rule: {rule_id} is a sensite port. Got port: {port}")
    except TypeError:
        pass

    return problems


def audit_firewall(rules: list[dict]) -> dict:
    results = {
        "audit_passed": False,
        "environment": None,
        "total_rules": 0,
        "valid_rules": 0,
        "invalid_rules": 0,
        "flagged_rules": [],
        "reasons": []
    }

    if not isinstance(rules, list):
        results["reasons"] = f"Rules must be a list, instead got: {type(rules).__name__}"
        return results
    
    results["total_rules"] = len(rules)
    environments = set()

    for rule in rules:
        if not isinstance(rule, dict):
            results["invalid_rules"] += 1
            results["flagged_rules"].append("<unknown>")
            results["reasons"].append(f"Each rule must be a dictionary, got {type(rule)}")
            continue
            
        rule_id = rule.get("rule_id", "<unknown>")
        environment = rule.get("environment")
        if environment is not None:
            environments.add(environment)
        
        # call validate_rule
        problems = validate_rule(rule)
        if problems:
            results["invalid_rules"] += 1
            results["flagged_rules"].append(rule_id)
            results["reasons"].extend(problems)
        else:
            results["valid_rules"] += 1
        
    if len(environments) == 1:
        results["environment"] = next(iter(environments))
    elif len(environments) > 1:
        results["environment"] = None
        results["reasons"].append(
        f"Rules belong to multiple environments: {sorted(environments)}"
        )
    else:
        results["reasons"].append("No environments found in rules")

    if (
        results["invalid_rules"] == 0
        and len(environments) == 1
        and results["environment"] == "production"
    ):
        results["audit_passed"] = True

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
        # rules = []  # prevent crash
    
    # # Debugging
    # for rule in rules:
    #     validate_rule(rule)

results = audit_firewall(rules)
print(json.dumps(results, indent=4))