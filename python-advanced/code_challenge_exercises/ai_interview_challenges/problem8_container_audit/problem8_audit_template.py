"""
DOCKER COMPOSE AUDIT — MID-LEVEL CHECKLIST

GOAL:
Implement a function that reads a Docker Compose YAML file and produces
service-focused audit metrics.

You are reviewing a Compose file to identify:
- how many services are defined
- which services are missing restart policies
- which services expose sensitive ports publicly
- which services use latest or unpinned images
- which environment variable names are reused across multiple services
- which services depend on services that do not exist

The YAML file is expected to contain a dictionary-based Docker Compose structure.

========================================================
1) FUNCTION SETUP
--------------------------------------------------------
[ ] Define: audit_docker_compose(file_path: str) -> dict

[ ] Initialize:
    - results (dict) for FINAL output:
        service_count -> int
        missing_restart_policy -> list[str]
        public_sensitive_ports -> dict[str, list[tuple[str, int]]]
        unpinned_images -> dict[str, str]
        shared_environment_variables -> dict[str, list[str]]
        undefined_dependencies -> dict[str, list[str]]

    - env_usage -> dict[str, set[str]]
    - defined_services -> set[str]
    - sensitive_container_ports -> set[int] with:
        {22, 2375, 2376, 3306, 5432, 6379, 27017}

========================================================
2) FILE HANDLING
--------------------------------------------------------
[ ] Use a try block

[ ] Open the file using a context manager

[ ] Load the YAML content into a dictionary

[ ] Handle:
    - file not found
    - invalid YAML
    - non-dictionary top-level YAML

[ ] On exception:
    - print an error message
    - return results

[ ] Hints for methods and functions to use here:
    - open()
    - yaml.safe_load()
    - isinstance()

========================================================
3) TOP-LEVEL EXTRACTION
--------------------------------------------------------
[ ] Extract:
    - services using a safe default of {}

[ ] If services is not a dictionary:
    return results

[ ] Set:
    - results["service_count"] to the number of services
    - defined_services to a set of the service names

[ ] Hints for methods and functions to use here:
    - dict.get()
    - isinstance()
    - len()
    - set()
    - dict.keys()

========================================================
4) SERVICE LOOP
--------------------------------------------------------
[ ] Iterate through services.items()

[ ] For each service_name and service_data:
    - skip non-dictionary service values

[ ] Extract with safe defaults:
    - image -> ""
    - ports -> []
    - environment -> []
    - depends_on -> []
    - restart -> None

[ ] Hints for methods and functions to use here:
    - dict.items()
    - isinstance()
    - dict.get()

========================================================
5) RESTART POLICY CHECK
--------------------------------------------------------
[ ] If restart is missing, empty, or not a string:
    - append service_name to results["missing_restart_policy"]

[ ] Hints for methods and functions to use here:
    - not
    - isinstance()
    - list.append()

========================================================
6) IMAGE PINNING CHECK
--------------------------------------------------------
[ ] If image is a non-empty string:

[ ] Mark the service in results["unpinned_images"] when:
    - image ends with ":latest"
    - or ":" is not in image

[ ] Store:
    - key -> service_name
    - value -> full image string

[ ] Hints for methods and functions to use here:
    - isinstance()
    - str.endswith()
    - in

========================================================
7) PORT AUDIT
--------------------------------------------------------
[ ] Only process ports if ports is a list

[ ] Loop through each port entry

[ ] Support only string port entries in this format:
    "host_port:container_port"

[ ] Skip entries that are not strings
[ ] Skip entries that do not contain ":"

[ ] Split the string into two parts only:
    - host part
    - container part

[ ] Convert host port to int
[ ] Convert container port to int

[ ] If conversion fails:
    continue

[ ] If:
    - host_port > 0
    - and container_port is in sensitive_container_ports

[ ] Then store a tuple in:
    results["public_sensitive_ports"][service_name]

[ ] The tuple should be:
    (original_port_string, container_port)

[ ] If service_name is not already in results["public_sensitive_ports"]:
    initialize it with an empty list

[ ] Hints for methods and functions to use here:
    - isinstance()
    - ":" in value
    - str.split(":", 1)
    - int()
    - try/except ValueError
    - dict.setdefault()
    - list.append()
    - set membership with in
    - tuple creation with ()

========================================================
8) ENVIRONMENT EXTRACTION
--------------------------------------------------------
[ ] Handle environment in two supported forms:

[ ] Case 1: environment is a list
    - each valid item is a string
    - use only items containing "="
    - split into key and value using one split only
    - keep only the key name

[ ] Case 2: environment is a dictionary
    - iterate through its keys
    - keep only string keys

[ ] For every extracted environment variable name:
    - if not already in env_usage:
        initialize with an empty set
    - add service_name to env_usage[variable_name]

[ ] Hints for methods and functions to use here:
    - isinstance()
    - list loop
    - dict.keys()
    - str.split("=", 1)
    - dict.setdefault()
    - set.add()

========================================================
9) DEPENDENCY CHECK
--------------------------------------------------------
[ ] Handle depends_on in two supported forms:

[ ] Case 1: depends_on is a list
    - use only string entries as dependency names

[ ] Case 2: depends_on is a dictionary
    - use its keys as dependency names

[ ] Build a temporary list of missing dependencies for the current service

[ ] For each dependency name:
    - if dependency_name is not in defined_services
    - append it to the missing list

[ ] If the missing list is not empty:
    - store the sorted missing list in
      results["undefined_dependencies"][service_name]

[ ] Hints for methods and functions to use here:
    - isinstance()
    - list.append()
    - dict.keys()
    - in
    - sorted()

========================================================
10) SHARED ENVIRONMENT VARIABLES
--------------------------------------------------------
[ ] Loop through env_usage.items()

[ ] For each variable_name and service_set:
    - if the number of services is greater than 1
    - store the sorted service names as a list in
      results["shared_environment_variables"][variable_name]

[ ] Hints for methods and functions to use here:
    - dict.items()
    - len()
    - sorted()
    - list()

========================================================
11) FINAL PROCESSING
--------------------------------------------------------
[ ] Sort:
    - results["missing_restart_policy"]

[ ] For each service in results["public_sensitive_ports"]:
    - sort the list of tuples

[ ] Hints for methods and functions to use here:
    - list.sort()
    - sorted()
    - dict loop

========================================================
12) RETURN VALUE
--------------------------------------------------------
[ ] Return results

========================================================
13) SCRIPT ENTRY POINT
--------------------------------------------------------
[ ] Add a main guard

[ ] Inside it:
    - define the sample file path
    - call the function
    - print the returned results

========================================================
Expected Result
--------------------------------------------------------
{
    "service_count": 5,
    "missing_restart_policy": [
        "db",
        "worker"
    ],
    "public_sensitive_ports": {
        "db": [
            ("5432:5432", 5432)
        ],
        "cache": [
            ("6379:6379", 6379)
        ]
    },
    "unpinned_images": {
        "web": "nginx:latest",
        "worker": "mycorp/worker"
    },
    "shared_environment_variables": {
        "APP_ENV": [
            "web",
            "worker"
        ],
        "LOG_LEVEL": [
            "web",
            "worker",
            "scheduler"
        ]
    },
    "undefined_dependencies": {
        "worker": [
            "queue"
        ]
    }
}
"""