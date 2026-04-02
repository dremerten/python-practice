"""
INTERVIEW CHALLENGE: FIREWALL RULE AUDIT

Implement exactly:
- validate_rule(rule: dict) -> list[str]
- audit_firewall(rules: list[dict]) -> dict

Also include these imports:
- import pprint
- import json

Do NOT change:
- constant names
- required keys
- sensitive port values
- error message text
- return structure
- field names

======================================================================
1) CONSTANTS
======================================================================

[ ] Define a constant set named SENSITIVE_PORTS with exactly these values:
    - 22
    - 3389
    - 5432
    - 3306
    - 6379

[ ] Define a constant set named REQUIRED_KEYS containing exactly these keys:
    - rule_id
    - environment
    - protocol
    - port
    - source
    - description
    - enabled

======================================================================
2) FUNCTION: validate_rule(rule)
======================================================================

GOAL
[ ] Validate one firewall rule
[ ] Return a list of problems
[ ] Return an empty list if the rule is valid

SETUP
[ ] Create a variable named problems
[ ] problems must start as an empty list

INPUT VALIDATION
[ ] Check whether rule is a dictionary
[ ] If rule is not a dictionary:
    [ ] Return EXACTLY:
        ["Invalid rule: not a dictionary"]

RULE ID
[ ] Read rule_id from rule
[ ] If rule_id is missing, use "<unknown>" as default value

REQUIRED KEYS
[ ] Create a variable named missing_keys
[ ] missing_keys must be computed as REQUIRED_KEYS - rule.keys()

[ ] If missing_keys is not empty:
    [ ] Append EXACTLY this string to problems:

        f"Rule {rule_id}: missing required keys: {sorted(missing_keys)}"

    [ ] Return problems immediately

----------------------------------------------------------------------
VALIDATIONS
Run the following checks in this exact order.
All messages in this section must be appended to problems.
----------------------------------------------------------------------

ENABLED
[ ] Evaluate rule["enabled"]

[ ] If rule["enabled"] is not True:
    [ ] Append EXACTLY this string:

        f"Rule {rule_id}: rule is not enabled"

PROTOCOL
[ ] Read protocol from rule["protocol"]

[ ] If protocol is not in {"tcp", "udp"}:
    [ ] Append EXACTLY this string:

        f"Rule {rule_id}: invalid protocol '{protocol}'"

PORT RANGE
[ ] Read port from rule["port"]

[ ] Use a try/except TypeError block

[ ] Inside the try block:
    [ ] Check whether port is less than 1 or greater than 65535

[ ] If port is less than 1 or greater than 65535:
    [ ] Append EXACTLY this string:

        f"Rule {rule_id}: port {port} is out of valid range"

[ ] Inside the except TypeError block:
    [ ] Append EXACTLY this string:

        f"Rule {rule_id}: invalid port value '{port}'"

PUBLIC SENSITIVE PORT EXPOSURE
[ ] Read source from rule["source"]

[ ] If source equals "0.0.0.0/0":
    [ ] Use a try/except TypeError block

[ ] Inside the try block:
    [ ] Check whether port is in SENSITIVE_PORTS

[ ] If port is in SENSITIVE_PORTS:
    [ ] Append EXACTLY this string:

        f"Rule {rule_id}: sensitive port {port} is publicly exposed"

[ ] Inside the except TypeError block:
    [ ] Do nothing
    [ ] Use pass

RETURN VALUE
[ ] Return problems

======================================================================
3) FUNCTION: audit_firewall(rules)
======================================================================

GOAL
[ ] Validate all firewall rules
[ ] Aggregate findings
[ ] Decide whether the firewall audit passes

RESULT STRUCTURE
[ ] Create a variable named result
[ ] result must start as EXACTLY:

    {
        "audit_passed": False,
        "environment": None,
        "total_rules": 0,
        "valid_rules": 0,
        "invalid_rules": 0,
        "flagged_rules": [],
        "reasons": [],
    }

INPUT VALIDATION
[ ] Check whether rules is a list

[ ] If rules is not a list:
    [ ] Append EXACTLY this string to result["reasons"]:

        "Invalid input: rules must be provided as a list"

    [ ] Return result immediately

INITIAL METRICS
[ ] Set result["total_rules"] to len(rules)

[ ] Create a variable named environments
[ ] environments must start as an empty set

LOOP THROUGH RULES
[ ] Process each rule in rules

FOR INVALID RULE ENTRIES
[ ] If a rule entry is not a dictionary:
    [ ] Increment result["invalid_rules"] by 1
    [ ] Append EXACTLY this string to result["flagged_rules"]:
        "<unknown>"
    [ ] Append EXACTLY this string to result["reasons"]:
        "Invalid rule: not a dictionary"
    [ ] Continue to the next rule

FOR VALID RULE ENTRIES
[ ] Read rule_id from the rule
[ ] If rule_id is missing, use "<unknown>"

[ ] Read environment from the rule
[ ] If environment is missing, use None

[ ] If environment is not None:
    [ ] Add environment to the environments set

RULE VALIDATION
[ ] Call validate_rule(rule)
[ ] Store the returned list in a variable named problems

CLASSIFICATION
[ ] If problems is not empty:
    [ ] Increment result["invalid_rules"] by 1
    [ ] Append rule_id to result["flagged_rules"]
    [ ] Extend result["reasons"] with all strings from problems

[ ] Otherwise:
    [ ] Increment result["valid_rules"] by 1

----------------------------------------------------------------------
POST-PROCESSING RULES
All messages in this section must be added to result["reasons"].
----------------------------------------------------------------------

ENVIRONMENT CONSISTENCY
[ ] If len(environments) == 1:
    [ ] Set result["environment"] to next(iter(environments))

[ ] Elif len(environments) > 1:
    [ ] Append EXACTLY this string to result["reasons"]:

        "Rules belong to multiple environments"

ENVIRONMENT REQUIREMENT
[ ] If result["environment"] != "production":
    [ ] Append EXACTLY this string to result["reasons"]:

        "Environment is not production"

FINAL DECISION
[ ] Set result["audit_passed"] to True only if ALL of the following are true:
    [ ] result["invalid_rules"] == 0
    [ ] len(environments) == 1
    [ ] result["environment"] == "production"

RETURN VALUE
[ ] Return result

======================================================================
4) MAIN EXECUTION BLOCK
======================================================================

[ ] Add this exact main guard:

    if __name__ == "__main__":

[ ] Inside it, use a try block

[ ] Open the file named "firewall_rules.json" in read mode

[ ] Load the JSON contents into a variable named rules using json.load(file)

[ ] Call audit_firewall(rules)
[ ] Store the returned value in a variable named result

[ ] Print the result using:
    pprint.pprint(result)

EXCEPTIONS
[ ] Add an except FileNotFoundError block
[ ] Print EXACTLY:
    "Error: firewall_rules.json file was not found."

[ ] Add an except json.JSONDecodeError block
[ ] Print EXACTLY:
    "Error: firewall_rules.json contains invalid JSON."

======================================================================
EXPECTED RESULTS
Using this firewall_rules.json input:
======================================================================

Expected output:

{
    "audit_passed": False,
    "environment": None,
    "total_rules": 6,
    "valid_rules": 3,
    "invalid_rules": 3,
    "flagged_rules": [
        "fw-002",
        "fw-005",
        "fw-006",
    ],
    "reasons": [
        "Rule fw-002: sensitive port 22 is publicly exposed",
        "Rule fw-005: invalid protocol 'icmp'",
        "Rule fw-005: port 0 is out of valid range",
        "Rule fw-006: sensitive port 3306 is publicly exposed",
        "Rules belong to multiple environments",
        "Environment is not production",
    ],
}
"""