import pprint
import json

SENSITE_PORTS = {22, 3389, 5432, 3306, 6379}
REQUIRED_KEYS = {
    "rule_id",
    "environment",
    "protocol",
    "port",
    "source",
    "description",
    "enabled"
}

def validate_rule(rule):
    problems = []

    if not isinstance(rule, dict):
        return ["Invalid rule: not a dictionary"]
    
    rule_id = rule.get("rule_id", "<unknown>")
    missing_keys = REQUIRED_KEYS - rule.keys()
    if missing_keys:
        problems.append(f"Rule {rule_id}: missing required keys: {sorted(missing_keys)}")

    if rule["enabled"] is not True:
        problems.append(f"Rule {rule_id}: rule is not enabled")
    
    protocol = rule.get("protocol")
    if protocol not in {"tcp", "udp"}:
        problems.append( f"Rule {rule_id}: invalid protocol '{protocol}'")
    
    port = rule.get("port")
    try:
        if port < 1 or port > 65535:
            problems.append(f"Rule {rule_id}: port {port} is out of valid range")
    except TypeError:
        problems.append(f"Rule {rule_id}: invalid port value '{port}'")

    source = rule["source"]
    if source == "0.0.0.0/0":
        try:
            if port in SENSITE_PORTS:
                problems.append(f"Rule {rule_id}: sensitive port {port} is publicly exposed")

        except TypeError:
            pass
    
    return problems


def audit_firewall(rules: list) -> dict:
    result =  {
        "audit_passed": False,
        "environment": None,
        "total_rules": 0,
        "valid_rules": 0,
        "invalid_rules": 0,
        "flagged_rules": [],
        "reasons": [],
    }

    if not isinstance(rules, list):
        result["reasons"].append("Invalid input: rules must be provided as a list")
        return result
    
    result["total_rules"] = len(rules)
    environments = set()

    for rule in rules:
        if not isinstance(rule, dict):
            result["invalid_rules"] += 1
            result["flagged_rules"].append("<unknown>")
            result["reasons"].append("Invalid rule: not a dictionary")
            continue

        rule_id = rule.get("rule_id", "<unknown>")
        environment = rule.get("environment", None)
        if environment is not None:
            environments.add(environment)
        
        problems = validate_rule(rule)
        if problems:
            result["invalid_rules"] += 1
            result["flagged_rules"].append(rule_id)
            result["reasons"].extend(problems)
        else:
            result["valid_rules"] += 1
    
    if len(environments) == 1:
        result[environment] = next(iter(environments))
    
    elif len(environments) > 1:
        result["reasons"].append("Rules belong to multiple environments")
    
    if result["environment"] != "production":
        result["reasons"].append("Environment is not production")
    
    if (
        result["invalid_rules"] == 0
        and len(environments) == 1
        and result["environment"] == "production"
    ):
        result["audit_passed"] = True
    
    return result



if __name__ == "__main__":
    try:
        with open("firewall_rules.json", 'r') as f:
            rules = json.load(f)       
            result= audit_firewall(rules)
            pprint.pprint(result)

    except FileNotFoundError:
        print(
            f"Error firewall_rules.json file was not found"
            )
    except json.JSONDecodeError:
        print(
            "Error: firewall_rules.json contains invalid JSON."
            )



### TO DEBUG ###
# with open("firewall_rules.json") as f:
#     rules = json.load(f)

# audit_firewall(rules)

# for rule in rules:
#     validate_rule(rule)