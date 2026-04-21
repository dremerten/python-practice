"""
# GOAL:
# Read a .env file line by line and produce an audit summary of its variables.
# You are reviewing the file to identify:
# - how many variables are defined
# - which variables have empty values
# - which variable names appear more than once
# - which variable names suggest sensitive data

# 1. Import modules
# 2. Define function: audit_env_file(file_path: str) -> dict
# 3. Initialize results dict:
#       total_variables -> int, starts at 0
#       empty_values -> list[str], starts as empty list
#       duplicate_variables -> list[str], starts as empty list
#       sensitive_variables -> list[str], starts as empty list
# 4. Initialize helpers:
#       seen_variables -> set() (tracks variable names already encountered)
#       duplicates -> set() (tracks variable names seen more than once)
#       sensitive_keywords -> list of strings to match against variable names ["PASSWORD", "SECRET", "KEY", "TOKEN"]

# 5. Open file in try/except block using context manager with utf-8 encoding
    # 6. Read file line by line
        # 7. Strip whitespace from each line
        # 8. Skip line if empty or starts with "#" (comments)
        # 9. Skip line if "=" not in line
        # 10. Split line on first "=" into key and value — strip whitespace from both
        # 11. Skip line if key is empty after stripping

        # 12. Increment results["total_variables"] by 1

        # 13. If value is empty string, append key to results["empty_values"]

        # 14. DUPLICATE TRACKING
        #       If key already in seen_variables, add key to duplicates set
        #       Otherwise add key to seen_variables

        # 15. SENSITIVE VARIABLE CHECK
        #       Uppercase the key
        #       If any keyword from sensitive_keywords is found in the uppercased key:
        #           append key to results["sensitive_variables"]

    # 16. POST-LOOP: assign sorted(duplicates) to results["duplicate_variables"]
    # 17. POST-LOOP: sort results["empty_values"] in place
    # 18. POST-LOOP: sort results["sensitive_variables"] in place

# 19. Catch FileNotFoundError — print message, return results
# 20. Catch unexpected Exception — print message, return results

# 21. Return results

# 22. Add main guard — call audit_env_file with ".env", print result using json.dumps with indent=4

# ========================================================
# Expected Result
# ========================================================
# {
#     "total_variables": 12,
#     "empty_values": [
#         "API_KEY",
#         "EMPTY_VALUE"
#     ],
#     "duplicate_variables": [
#         "DB_PASSWORD"
#     ],
#     "sensitive_variables": [
#         "API_KEY",
#         "DB_PASSWORD",
#         "DB_PASSWORD",
#         "SERVICE_TOKEN"
#     ]
# }
"""