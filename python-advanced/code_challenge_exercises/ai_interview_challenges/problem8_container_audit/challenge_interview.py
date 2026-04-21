"""
# 1. Import modules
# 2. Define function with type hints
# 3. Initialize results dict (service_count, missing_restart_policy, public_sensitive_ports, unpinned_images, shared_environment_variables, undefined_dependencies)
# 4. Initialize helpers:
#       env_usage -> dict[str, set[str]] (tracks which services use each env variable name)
#       defined_services -> set[str] (all service names that exist in the file)
#       sensitive_container_ports -> set[int] {22, 2375, 2376, 3306, 5432, 6379, 27017}

# 5. Open entire function body in a single try block
#       with open(file_path) to load YAML using yaml.safe_load()
#       If top-level result is not a dictionary — print message, return results
#       Extract services from top-level dict (default {})
#       If services is not a dictionary — return results

# 6. Set results["service_count"] to len(services)
# 7. Set defined_services to a set of all keys in services

# 8. Iterate through services.items() to get (service_name, service_data) pairs
    # 9. Skip service if service_data is not a dictionary

    # 10. Extract from service_data with safe defaults:
    #       image -> ""
    #       ports -> []
    #       environment -> []
    #       depends_on -> []
    #       restart -> None

    # 11. RESTART POLICY CHECK
    #       If restart is missing or not a string, append service_name to results["missing_restart_policy"]

    # 12. IMAGE PINNING CHECK
    #       If image is a non-empty string and ends with ":latest" OR does not contain ":":
    #       store in results["unpinned_images"] as {service_name: image}

    # 13. PORT AUDIT
    #       If ports is a list, loop through each port_entry:
        # 14. Skip port_entry if not a string or does not contain ":"
        # 15. Split port_entry on ":" into host_port_str and container_port_str
        # 16. Convert both to int inside try/except — skip this port_entry on ValueError
        # 17. If host_port > 0 AND container_port is in sensitive_container_ports:
        #       use setdefault(service_name, []) to ensure the list exists in results["public_sensitive_ports"]
        #       append (port_entry, container_port) tuple to results["public_sensitive_ports"][service_name]

    # 18. ENVIRONMENT EXTRACTION
    #       If environment is a list:
        # 19. Loop through each item — skip if not a string or does not contain "="
        # 20. Split item on first "=" using split("=", 1), unpack as variable_name and _ (discard right side)
        # 21. Use env_usage.setdefault(variable_name, set()), then add service_name to that set
    #       If environment is a dict:
        # 22. Loop through keys as variable_name — skip if not a string
        # 23. Use env_usage.setdefault(variable_name, set()), then add service_name to that set

    # 24. DEPENDENCY CHECK
    #       Initialize missing_dependencies = []
    #       If depends_on is a list:
        # 25. Loop through each dependency_name — skip if not a string
        # 26. If dependency_name not in defined_services, append to missing_dependencies
    #       If depends_on is a dict:
        # 27. Loop through its keys as dependency_name
        # 28. If dependency_name not in defined_services, append to missing_dependencies
    # 29. If missing_dependencies is non-empty, store sorted(missing_dependencies) in results["undefined_dependencies"][service_name]

# 30. POST-LOOP: iterate env_usage.items() — for each (variable_name, service_set), if len(service_set) > 1 store sorted(service_set) in results["shared_environment_variables"][variable_name]
# 31. POST-LOOP: sort results["missing_restart_policy"] in place
# 32. POST-LOOP: loop through results["public_sensitive_ports"].items() — for each (service_name, port_list), call port_list.sort() to sort tuples in place

# 33. Return results

# 34. Catches at the bottom of the try block:
#       except FileNotFoundError — print message, return results
#       except yaml.YAMLError — print message, return results
#       except Exception — print message, return results

# 35. Add main guard — define sample file path, call function, print results

# ========================================================
# Expected Result
# ========================================================
# {
#     "service_count": 5,
#     "missing_restart_policy": ["db", "worker"],
#     "public_sensitive_ports": {
#         "db": [("5432:5432", 5432)],
#         "cache": [("6379:6379", 6379)]
#     },
#     "unpinned_images": {
#         "web": "nginx:latest",
#         "worker": "mycorp/worker",
#         "cache": "redis:latest"
#     },
#     "shared_environment_variables": {
#         "APP_ENV": ["web", "worker"],
#         "LOG_LEVEL": ["cache", "scheduler", "web", "worker"]
#     },
#     "undefined_dependencies": {
#         "worker": ["queue"]
#     }
# }
"""