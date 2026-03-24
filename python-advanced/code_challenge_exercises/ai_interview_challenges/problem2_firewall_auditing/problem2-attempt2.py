"""
This script audits inbound firewall rules from a JSON file and determines whether
a production network is safely configured. Each rule must be validated for risk,
and the overall audit should fail if dangerous ports are publicly exposed.
The goal is to identify unsafe rules and return a clear security summary.
"""

import pprint
import json

SENSITIVE_PORTS = {22, 3389, 5432, 3306, 6379}
REQUIRED_KEYS = {
    "rule_id",
    "environment",
    "protocol",
    "port",
    "source",
    "description",
    "enabled",
}


def validate_rule(rule: dict) -> list[str]:
    # TODO: initialize problems list
    problems = []
    rule_id, environment, protocol, port, source, description, enabled = (
        rule["rule_id"],
        rule["environment"],
        rule["protocol"],
        rule["port"],
        rule["source"],
        rule["description"],
        rule["enabled"]
    )

    # TODO: if rule is not a dict:
    # - return ["Invalid rule: not a dictionary"]
    if not isinstance(rule, dict):
        return ["Invalid rule: not a dictionary"]

    # TODO: extract rule_id with default "<unknown>"
    rule_id = rule.get("rule_id", "<unknown>")

    # TODO: compute missing_keys from REQUIRED_KEYS
    # - if missing_keys:
    #     - append problem message
    #     - return problems
    missing_keys = REQUIRED_KEYS - rule.keys()
    if missing_keys:
        problems.append(
            f"Rule {rule_id} is missing required keys: {sorted(missing_keys)}"
            )
        return problems

    # TODO: check if rule["enabled"] is enabled(True)
    # - if not True:
    #     - append problem
    if rule["enabled"] is not True:
        problems.append(f"Missing rule dictionary")

    # TODO: validate protocol
    # - if protocol is not "tcp" and not "udp":
    #     - append problem
    if protocol not in {"tcp", "udp"}:
        problems.append(f"Rule {rule_id}: invalid protocol '{protocol}'")

    # TODO: validate port
    # - try:
    #     - if port is less than 1 or greater than 65535:
    #         - append problem
    # - except TypeError:
    #     - append invalid value problem
    try:
        if port < 1 or port > 65535:
            problems.append(f"Rule {rule_id}: port {port} is out of valid range")
    except TypeError:
        problems.append(f"Rule {rule_id}: invalid port value '{port}'")

    # TODO: check if source is publicly open
    # - if source == "0.0.0.0/0":
    #     - if port is in SENSITIVE_PORTS:
    #         - append problem
    if source == "0.0.0.0/0":
        if port in SENSITIVE_PORTS:
            problems.append(f"Rule {rule_id}: sensitive port {port} is publicly exposed")

    # TODO: return problems
    return problems


def audit_firewall(rules: list[dict]) -> dict:
    # TODO: initialize result dictionary with default values
    result = {
    "audit_passed": False,
    "environment": None,
    "total_rules": 0,
    "valid_rules": 0,
    "invalid_rules": 0,
    "flagged_rules": [],
    "reasons": [],
    }

    # TODO: if rules is not a list:
    # - append reason
    # - return result
    if not isinstance(rules, list):
        result["reasons"].append("Invalid input: rules must be provided as a list")
        return result

    # TODO: set result["total_rules"] to the number of rules
    result["total_rules"] = len(rules)

    # TODO: initialize environments set
    environments = set()

    # TODO: iterate through rules
    # - if rule is not a dict:
    #     - increment invalid_rules
    #     - append "<unknown>" to flagged_rules
    #     - append reason "Invalid rule: not a dictionary"
    #     - continue
    for rule in rules:
        if not isinstance(rule, dict):
            result["invalid_rules"] += 1
            result["flagged_rules"].append("<unknown>")
            result["reasons"].append(f"Invalid rule: not a dictionary")
            continue

        # - extract rule_id with default "<unknown>"
        # - extract environment
        rule_id = rule.get("rule_id", "<unknown>")
        environment = rule.get("environment")

        # - if environment is not None:
        #     - add to environments set
        if environment is not None:
            environments.add(environment)

        # - call validate_rule(rule) assign to problems variable
        problems = validate_rule(rule)

        # - if problems exist:
        #     - increment invalid_rules
        #     - append rule_id to flagged_rules
        #     - extend reasons with problems
        # - else:
        #     - increment valid_rules
        if problems:
            result["invalid_rules"] += 1
            result["flagged_rules"].append(rule_id)
            result["reasons"].extend(problems)
        else:
            result["valid_rules"] += 1

    # TODO: evaluate environments
    # - if len(environments) == 1:
    #     - set result["environment"] = next(iter(environments))
    # - elif len(environments) > 1:
    #     - append reason "Rules belong to multiple environments"
    if len(environments) == 1:
        result["environment"] = next(iter(environments))
    elif len(environments) > 1:
        result["reasons"].append("Rules belong to multiple environments")

    # TODO: check if environment != "production"
    # - append reason if true
    if result["environment"] != "production":
        result["reasons"].append(f"Environment does not match 'production'")

    # TODO: final audit decision
    # - if invalid_rules == 0
    #   and len(environments) == 1
    #   and result["environment"] == "production":
    #     - set result["audit_passed"] = True
    if (
        result["invalid_rules"] == 0
        and len(environments) == 1
        and result["environment"] == "production"
    ):
        result["audit_passed"] = True
        
    # TODO: return result
    return result


if __name__ == "__main__":
    # TODO: open "firewall_rules.json" file
    # - load JSON data into rules
    PATH = "firewall_rules.json"
    try:
        with open(PATH) as f:
            rules = json.load(f)

        # TODO: call audit_firewall(rules)
        # TODO: pretty print result using pprint
        result = audit_firewall(rules)
        pprint.pprint(result, indent=4)
   
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Missing file: {PATH}") from e

    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {PATH}") from e



    



