"""
=============================================================================
CODING CHALLENGE: Firewall Rule Audit
=============================================================================

Your security team needs an automated way to audit firewall rules before
approving them for production. You will receive a list of firewall rule
dictionaries loaded from a JSON file. Your job is to validate each rule
individually, then produce an overall audit report for the entire ruleset.

An example firewall rule looks like this:

    {
        "rule_id": "fw-001",
        "environment": "production",
        "protocol": "tcp",
        "port": 443,
        "source": "0.0.0.0/0",
        "description": "Allow HTTPS",
        "enabled": true
    }

A template has been provided for you. Do NOT redefine the imports, constants,
function signatures, or the main block structure -- they are already in place.
Your job is to fill in the bodies of the two functions and complete the main
block where indicated.

=============================================================================
PART 1: validate_rule(rule)
=============================================================================

The function signature, the problems list, the isinstance check, and the
return statement are already written. Your job is to fill in everything
between the isinstance check and the return.

  RULE ID
    Read rule_id from rule using a fallback of "<unknown>" in case the key
    is missing. You will use this in every error message throughout the function.

  REQUIRED KEYS
    Compute missing_keys as the set difference between REQUIRED_KEYS and the
    keys present in the rule. If any keys are missing, append a reason using
    sorted(missing_keys) in the message and return problems immediately --
    do not continue checking a rule that is structurally incomplete.

  ENABLED CHECK
    Check whether rule["enabled"] is exactly the boolean True using identity
    comparison -- not just truthy. If it is not True, append a reason.

  PROTOCOL CHECK
    Read the protocol value. If it is not in the set of valid protocols,
    append a reason that includes the actual protocol value found.
    Valid protocols are "tcp" and "udp" only.

  PORT RANGE CHECK -- wrap this entire block in a try/except TypeError
    Read the port value. Check whether it is less than 1 OR greater than 65535.
    If it is out of range, append a reason that includes the port value.
    If a TypeError is raised (port is not comparable to a number), append
    a reason that says the port value is invalid and include the value.

  SENSITIVE PORT EXPOSURE CHECK
    This check only applies when source equals "0.0.0.0/0".
    If source is "0.0.0.0/0", wrap the following in a try/except TypeError:
      Check whether port is in SENSITIVE_PORTS. If it is, append a reason
      that includes the port number.
      If a TypeError is raised, use pass -- silently ignore it and move on.

=============================================================================
PART 2: audit_firewall(rules)
=============================================================================

The function signature and return statement are already written. results is
initialized as an empty dict. Your first task is to remove the breakpoint()
and replace results = {} with the full initialized result dictionary. Then
fill in all the logic between initialization and the return.

  The result dictionary MUST contain these exact keys:
    - audit_passed    -> boolean, start as False
    - environment     -> start as None
    - total_rules     -> start as 0
    - valid_rules     -> start as 0
    - invalid_rules   -> start as 0
    - flagged_rules   -> start as empty list
    - reasons         -> start as empty list

  Structure guidance:

  PHASE 1 -- Replace results = {} with the fully initialized result dict.
    Remove the breakpoint(). This dict is your return value no matter what.

  PHASE 2 -- Validate the input itself.
    Before looping, confirm that rules is actually a list. If it is not,
    append a reason and return early.

  PHASE 3 -- Set total_rules.
    Assign the length of the rules list before entering the loop.

  PHASE 4 -- Track environments across rules.
    You need to detect whether all rules share the same environment or
    belong to multiple. Use a data structure that only stores unique values.
    You will use this after the loop to resolve results["environment"].

  PHASE 5 -- Loop through each rule.
    For each item in the list, handle these cases in order:

      a) If the item is not a dict -- increment invalid_rules, append
         "<unknown>" to flagged_rules, append a reason, then skip to the
         next item with continue.

      b) Get the rule_id with a fallback of "<unknown>".

      c) Get the environment value. If it is not None, add it to your
         environment tracker.

      d) Call validate_rule() on the rule. If problems were returned,
         increment invalid_rules, append rule_id to flagged_rules, and
         add all problems to reasons -- you are adding a list of strings
         to another list, so pick the right method. If no problems were
         returned, increment valid_rules.

  PHASE 6 -- Resolve the environment after the loop.
    Look at your environments set. If it has exactly one item, 
    pull that value out using next(iter(...)) and assign it to results["environment"]. 
    If it has more than one item, the ruleset spans multiple environments 
    — append a reason that makes this clear and includes which environments were found.

  PHASE 7 -- Environment requirement check.
    If results["environment"] is not "production", append a reason.

  PHASE 8 -- Set audit_passed.
    Only set it to True if ALL of the following are true at once:
      - invalid_rules is exactly 0
      - exactly one unique environment was seen
      - that environment is "production"
    Use a single compound if statement, not nested ifs.

  PHASE 9 -- Return the result dict.

=============================================================================
PART 3: main block
=============================================================================

The file path, try/except, and debug loop are already written. Note how the
two exceptions are handled -- they are not symmetrical:
  - FileNotFoundError raises immediately with a message
  - json.JSONDecodeError prints a message and sets rules to an empty list
    so the rest of the program can continue without crashing

The debug loop calls validate_rule() on each rule but does not print the
result. You can add a print() around it while testing to see output.

The last line calls audit_firewall(rules) but does not store or print the
result. Update this line to store the return value in a variable named result
and print it using json.dumps() with an indent of 4. json is already imported.

=============================================================================
CLARIFICATIONS (questions you would ask the interviewer):
=============================================================================

Q: What makes a firewall rule valid?
A: A valid rule must meet ALL of the following:
     - It is enabled (exactly the boolean True, not just truthy)
     - Protocol is either "tcp" or "udp" -- nothing else
     - Port is a number between 1 and 65535 inclusive
     - If the source is "0.0.0.0/0" (publicly exposed), the port must not
       be a sensitive port

Q: What are the sensitive ports?
A: 22, 3389, 5432, 3306, and 6379. These are already defined in SENSITIVE_PORTS.

Q: What conditions must be true for the audit to pass?
A: All rules must be valid, all rules must belong to the same environment,
   and that environment must be "production". There is no minimum rule count.

Q: How should I handle bad data -- missing keys, wrong types, non-dict entries?
A: Treat them as invalid rules. Capture the problem in your reasons list
   rather than letting the function crash.

Q: Should I use try/except blocks?
A: Yes, in exactly two places inside validate_rule:

     1. Port range check -- wrap the comparison in try/except TypeError.
        If port is a string or None, the comparison port < 1 will raise
        a TypeError. Catch it and append an "invalid port value" message.

     2. Sensitive port exposure check -- also wrap in try/except TypeError.
        If port is not hashable or comparable, the "in" check can fail.
        If a TypeError occurs here, use pass -- silently ignore and move on.

   Keep both try blocks as narrow as possible -- only wrap the line that
   can actually raise the exception.

Q: What exact error messages should I use?
A: Use these exactly -- spelling, quotes, and formatting all matter:
     - Missing keys:       "Rule {rule_id}: missing required keys: {sorted(missing_keys)}"
     - Not enabled:        "Rule {rule_id}: rule is not enabled"
     - Invalid protocol:   "Rule {rule_id}: invalid protocol '{protocol}'"
     - Port out of range:  "Rule {rule_id}: port {port} is out of valid range"
     - Invalid port value: "Rule {rule_id}: invalid port value '{port}'"
     - Sensitive exposure: "Rule {rule_id}: sensitive port {port} is publicly exposed"
     - Not a dictionary:   "Invalid rule: not a dictionary"
     - Multiple envs:      "Rules belong to multiple environments"
     - Wrong environment:  "Environment is not production"
     - Invalid input:      "Invalid input: rules must be provided as a list"


=============================================================================
EXPECTED OUTPUT
Using the provided firewall_rules.json:
=============================================================================

{'audit_passed': False,
 'environment': None,
 'flagged_rules': ['fw-002',
                   'fw-005',
                   'fw-006',
                   'fw-011',
                   'fw-013',
                   'fw-015',
                   'fw-023',
                   'fw-024',
                   'fw-025',
                   'fw-026'],
 'invalid_rules': 10,
 'reasons': ['Rule fw-002: sensitive port 22 is publicly exposed',
             "Rule fw-005: invalid protocol 'icmp'",
             'Rule fw-005: port 0 is out of valid range',
             'Rule fw-006: sensitive port 3306 is publicly exposed',
             'Rule fw-011: sensitive port 3389 is publicly exposed',
             'Rule fw-013: sensitive port 6379 is publicly exposed',
             'Rule fw-015: port 70000 is out of valid range',
             'Rule fw-023: rule is not enabled',
             "Rule fw-024: invalid protocol 'FTP'",
             'Rule fw-025: port -1 is out of valid range',
             'Rule fw-026: sensitive port 5432 is publicly exposed',
             'Rules belong to multiple environments',
             'Environment is not production'],
 'total_rules': 34,
 'valid_rules': 24}

Why each field has the value it does:
  - audit_passed is False -- invalid rules exist and environments are mixed
  - environment is None -- fw-006 and fw-027 are staging; two environments
    were seen so it cannot resolve to a single value
  - total_rules is 34 -- all 34 rules in the file were counted
  - valid_rules is 23 -- rules with no problems of any kind
  - invalid_rules is 11 -- each had at least one problem
  - reasons has 14 entries -- 12 from individual rule validation (fw-005
    contributes two), 2 from fleet-level environment checks after the loop

=============================================================================
THINGS TO WATCH OUT FOR
=============================================================================

  1. The missing keys check uses set difference (REQUIRED_KEYS - rule.keys()).
     The result is a set. Wrap it in sorted() in the error message so the
     output is deterministic and matches the expected results.

  2. The enabled check uses "is not True" -- not "!= True". A value of 1
     would pass != True but fail "is not True". Be intentional.

  3. The sensitive port check only runs when source is exactly "0.0.0.0/0".
     A sensitive port behind an internal CIDR is not a problem. See fw-003
     -- it has port 5432 (a sensitive port) but is still valid because the
     source is an internal address.

  4. Port 0 is out of range. Valid range is 1 to 65535 inclusive.
     The lower bound check is port < 1.

  5. fw-005 produces two problems from a single rule -- invalid protocol AND
     port out of range. Make sure you are not returning early after the first
     problem is found. The only early return in validate_rule should be after
     the missing keys check.

  6. The environment field stays None when multiple environments are seen --
     not an empty string, not a list. The "exactly one" branch never runs so
     it keeps its initialized value.

  7. The debug loop in the template calls validate_rule() but does not print
     anything. Wrap the call in print() while testing so you can see output.

=============================================================================
"""