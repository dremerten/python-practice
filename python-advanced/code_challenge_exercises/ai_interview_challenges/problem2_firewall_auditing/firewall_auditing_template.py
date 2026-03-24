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

    # TODO: if rule is not a dict:
    # - return ["Invalid rule: not a dictionary"]

    # TODO: extract rule_id with default "<unknown>"

    # TODO: compute missing_keys from REQUIRED_KEYS
    # - if missing_keys:
    #     - append problem message
    #     - return problems

    # TODO: check if rule["enabled"] is enabled(True)
    # - if not True:
    #     - append problem

    # TODO: validate protocol
    # - if protocol is not "tcp" and not "udp":
    #     - append problem

    # TODO: validate port
    # - try:
    #     - if port is less than 1 or greater than 65535:
    #         - append problem
    # - except TypeError:
    #     - append invalid value problem

    # TODO: check if source is publicly open
    # - if source == "0.0.0.0/0":
    #     - if port is in SENSITIVE_PORTS:
    #         - append problem

    # TODO: return problems
    return problems


def audit_firewall(rules: list[dict]) -> dict:
    # TODO: initialize result dictionary with default values
    result = {
    "audit_passed": bool,
    "environment": str | None,
    "total_rules": int,
    "valid_rules": int,
    "invalid_rules": int,
    "flagged_rules": list[str],
    "reasons": list[str],
    }

    # TODO: if rules is not a list:
    # - append reason
    # - return result

    # TODO: set result["total_rules"] to the number of rules

    # TODO: initialize environments set

    # TODO: iterate through rules
    # - if rule is not a dict:
    #     - increment invalid_rules
    #     - append "<unknown>" to flagged_rules
    #     - append reason "Invalid rule: not a dictionary"
    #     - continue

        # - extract rule_id with default "<unknown>"
        # - extract environment

        # - if environment is not None:
        #     - add to environments set

        # - call validate_rule(rule) assign to problems variable

        # - if problems exist:
        #     - increment invalid_rules
        #     - append rule_id to flagged_rules
        #     - extend reasons with problems
        # - else:
        #     - increment valid_rules

    # TODO: evaluate environments
    # - if len(environments) == 1:
    #     - set result["environment"] = next(iter(environments))
    # - elif len(environments) > 1:
    #     - append reason "Rules belong to multiple environments"

    # TODO: check if environment != "production"
    # - append reason if true

    # TODO: final audit decision
    # - if invalid_rules == 0
    #   and len(environments) == 1
    #   and result["environment"] == "production":
    #     - set result["audit_passed"] = True

    # TODO: return result
    return result


if __name__ == "__main__":
    # TODO: open "firewall_rules.json" file
    # - load JSON data into rules

    # TODO: call audit_firewall(rules)

    # TODO: pretty print result using pprint
    pass