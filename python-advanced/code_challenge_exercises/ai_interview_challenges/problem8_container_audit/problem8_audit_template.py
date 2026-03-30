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

Hints for methods and functions to use here:
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
    - results["service_count"] to how many services are defined
    - defined_services to a set of the service names (the dictionary’s keys)

Hints for methods and functions to use here:
    - dict.get()
    - isinstance()
    - len()
    - set()
    - dict.keys()

========================================================
4) SERVICE LOOP
--------------------------------------------------------
[ ] Iterate through the services dictionary to access both service_name and service_data

[ ] For each service_name and service_data:
    - skip entries where service_data is not a dictionary

[ ] Extract with safe defaults:
    - image -> ""
    - ports -> []
    - environment -> []
    - depends_on -> []
    - restart -> None

Hints for methods and functions to use here:
    dict.items()
    isinstance()
    dict.get()

========================================================
5) RESTART POLICY CHECK
--------------------------------------------------------
[ ] If restart is missing, empty, or not a string:
    - append service_name to results["missing_restart_policy"]

Hints for methods and functions to use here:
    not
    isinstance()
    list.append()

========================================================
6) IMAGE PINNING CHECK
--------------------------------------------------------
[ ] If image is a non-empty string:

[ ] Mark the service in results["unpinned_images"] when:
    - image ends with ":latest"
    - or ":" is not in image

[ ] If the image is unpinned (ends with ":latest" or has no tag):
    - record it in results["unpinned_images"] with:
        key = service_name
        value = image string

Hints for methods and functions to use here:
    isinstance()
    str.endswith()
    in

========================================================
7) PORT AUDIT
--------------------------------------------------------
[ ] Only continue if `ports` is a list
[ ] Loop through each item in `ports`, call it `port_entry`
[ ] Skip `port_entry` if it is not a string
[ ] Skip `port_entry` if it does not contain a colon ":"
[ ] Split `port_entry` using `split(":", 1)` and assign:
      - left part -> `host_port_str`
      - right part -> `container_port_str`
[ ] Convert `host_port_str` to integer `host_port` inside try/except
[ ] Convert `container_port_str` to integer `container_port` inside try/except
[ ] If conversion fails, skip this `port_entry`
[ ] Write an if statement to check:
      host_port > 0 AND container_port is in sensitive_container_ports
      - Inside the if:
          * Ensure results["public_sensitive_ports"][service_name] exists as a list
            Hint: use setdefault(service_name, [])
          * Append a tuple `(port_entry, container_port)` to the list for that `service_name`

========================================================
8) ENVIRONMENT EXTRACTION
--------------------------------------------------------
Only process `environment` if it is a list or a dict

[ ] Case 1: `environment` is a list
    - Loop through each item, call it `item`
    - Skip `item` if it is not a string
    - Skip `item` if it does not contain "="
    - Split `item` at the first "=" using `split("=", 1)`:
          * left part -> `variable_name`
          * right part -> `_` (use `_` to ignore the value)
    - Ensure `env_usage[variable_name]` exists as a set
          * Hint: use setdefault(variable_name, set())
    - Add `service_name` to `env_usage[variable_name]`

[ ] Case 2: `environment` is a dict
    - Loop through its keys, call each key `variable_name`
    - Skip `variable_name` if it is not a string
    - Ensure `env_usage[variable_name]` exists as a set
          * Hint: use setdefault(variable_name, set())
    - Add `service_name` to `env_usage[variable_name]`

========================================================
9) DEPENDENCY CHECK
--------------------------------------------------------
[ ] Create a list called `missing_dependencies`

Only process `depends_on` if it is a list or a dict

[ ] Case 1: `depends_on` is a list
    - Loop through each item in depends_on, call it `dependency_name`
    - Skip `dependency_name` if it is not a string
    - If `dependency_name` is not in `defined_services`, append it to `missing_dependencies`

[ ] Case 2: `depends_on` is a dict
    - Loop through its keys, call each key `dependency_name`
    - If `dependency_name` is not in `defined_services`, append it to `missing_dependencies`

[ ] After processing all dependencies:
    - If `missing_dependencies` contains any items:
          * Store a **sorted copy** in `results["undefined_dependencies"][service_name]
========================================================
10) SHARED ENVIRONMENT VARIABLES
--------------------------------------------------------
[ ] Loop through `env_usage.items()`, unpack as `variable_name` and `service_set`

[ ] For each `variable_name` and `service_set`:
    - If `len(service_set)` > 1
    - Assign `results["shared_environment_variables"][variable_name] = sorted(service_set)`
      (sorting converts the set into a list in place of the assignment)

11) FINAL PROCESSING
--------------------------------------------------------
[ ] Sort the list `results["missing_restart_policy"]` in place

[ ] Loop through each `service_name` in `results["public_sensitive_ports"]`:
    - Sort the list of tuples `results["public_sensitive_ports"][service_name]` in place

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