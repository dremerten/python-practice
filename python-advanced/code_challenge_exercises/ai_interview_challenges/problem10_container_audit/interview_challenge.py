"""
# GOAL:
# Read a JSON file containing a list of container deployment configs and produce
# an audit summary identifying invalid containers and deployment-level problems.
#
# You are reviewing containers to identify:
# - containers missing required keys
# - containers running in privileged mode
# - containers using disallowed image tags
# - containers with invalid restart policies
# - containers with invalid cpu_limit values
# - containers with invalid memory_limit formats
# - whether all containers belong to the same environment
# - whether the deployment environment is production

# ========================================================
# MODULE-LEVEL CONSTANTS (defined outside any function)
# ========================================================
# DISALLOWED_TAGS          -> set containing "latest"
# REQUIRED_KEYS            -> set of 8 strings:
#                             "container_id", "environment", "image", "tag",
#                             "privileged", "restart_policy", "cpu_limit", "memory_limit"
# ALLOWED_RESTART_POLICIES -> set containing "always", "unless-stopped", "on-failure"
# ALLOWED_MEMORY_SUFFIXES  -> tuple containing ("Mi", "Gi")

# ========================================================
# FUNCTION 1: validate_container(container: dict) -> list[str]
# ========================================================
# 1. Initialize problems = []
# 2. If container is not a dict, return ["Invalid container: not a dictionary"]
# 3. Extract container_id using .get("container_id", "<unknown>")

# 4. MISSING KEYS CHECK
#       missing_keys = REQUIRED_KEYS - container.keys()
#       If non-empty: append problem string with sorted(missing_keys), return problems early

# 5. PRIVILEGED CHECK
#       container["privileged"] must be exactly False — use `is not False`

# 6. TAG CHECK
#       container["tag"] must not be in DISALLOWED_TAGS

# 7. RESTART POLICY CHECK
#       container["restart_policy"] must be in ALLOWED_RESTART_POLICIES

# 8. CPU LIMIT CHECK
#       container["cpu_limit"] must be > 0
#       Wrap comparison in try/except TypeError — value may not be comparable

# 9. MEMORY LIMIT CHECK
#       If memory_limit is not a string: append problem string
#       Else if memory_limit ends with a valid suffix in ALLOWED_MEMORY_SUFFIXES:
#           slice off last 2 characters to get numeric_part
#           inside try/except ValueError:
#               convert numeric_part to int — if <= 0: append problem string
#           on ValueError: append problem string (numeric part is not a valid integer)
#       Else (no valid suffix): append problem string

# 10. Return problems

# ========================================================
# FUNCTION 2: audit_deployments(containers: list[dict]) -> dict
# ========================================================
# 11. Initialize result dict:
#       audit_passed            -> False
#       environment             -> None
#       total_containers        -> 0
#       valid_containers        -> 0
#       invalid_containers      -> 0
#       flagged_containers      -> []
#       reasons                 -> []

# 12. If containers is not a list: append problem to reasons, return result early
# 13. Set result["total_containers"] = len(containers)
# 14. Initialize environments = set()

# 15. Loop through each container:
#       If not a dict: increment invalid_containers, append "<unknown>" to flagged_containers, append problem to reasons, continue
#       Extract container_id using .get("container_id", "<unknown>")
#       Extract environment using .get("environment", None)
#       If environment is not None: add to environments set
#       Call validate_container(container) -> problems
#       If problems: increment invalid_containers, append container_id to flagged_containers, extend reasons with problems
#       Else: increment valid_containers

# 16. POST-LOOP ENVIRONMENT CHECK
#       If len(environments) == 1: set result["environment"] = next(iter(environments))
#       If len(environments) > 1: append problem string to reasons
#       If result["environment"] != "production": append problem string to reasons

# 17. POST-LOOP AUDIT PASSED CHECK
#       True only 
#   - if invalid_containers == 0 AND 
#   - len(environments) == 1 AND 
#   - environment == "production"

# 18. Return result

# ========================================================
# MAIN GUARD
# ========================================================
# 19. Open "container_deployments.json" in try/except block
#       Load JSON using json.load()
#       Call audit_deployments() and pretty print result using pprint.pprint()
#       Catch FileNotFoundError — print message
#       Catch json.JSONDecodeError — print message

# ========================================================
# Expected Result
# ========================================================
# {
#     "audit_passed": False,
#     "environment": None,
#     "flagged_containers": ["ctr-002", "ctr-003", "ctr-005"],
#     "invalid_containers": 3,
#     "reasons": [
#         "Container ctr-002: disallowed tag 'latest'",
#         "Container ctr-003: privileged mode must be disabled",
#         "Container ctr-005: invalid restart policy 'sometimes'",
#         "Container ctr-005: cpu_limit -1 must be greater than 0",
#         "Container ctr-005: invalid memory_limit '2048'",
#         "Containers belong to multiple environments",
#         "Environment is not production"
#     ],
#     "total_containers": 6,
#     "valid_containers": 3
# }
"""