import json


DISALLOWED_TAGS = {"latest"}

REQUIRED_KEYS = {
    "container_id",
    "environment",
    "image", 
    "tag", 
    "privileged", 
    "restart_policy",
    "cpu_limit", 
    "memory_limit"
}

ALLOWED_RESTART_POLICIES = {"always", "unless-stopped", "on-failure"}

ALLOWED_MEMORY_SUFFIXES = ("Mi", "Gi")



def validate_container(container: dict) -> list[str]:
    problems = []

    if not isinstance(container, dict):
        return ["Invalid container: not a dictionary"]

    container_id = container.get("container_id", "<unknown>")

    missing_keys = REQUIRED_KEYS - container.keys()
    if missing_keys:
        problems.append(f"Missing required keys: {sorted(missing_keys)}")
        return problems
    
    if container["privileged"] is not False:
        problems.append(f"Container {container_id}: privileged mode must be disabled")

    if container["tag"] in DISALLOWED_TAGS:
        problems.append(f"{container_id} is using a disallowed tag: {container["tag"]}")

    if container["restart_policy"] not in ALLOWED_RESTART_POLICIES:
        problems.append(f"{container_id} restart policy is invalid: {container["restart_policy"]}")

    cpu_limit = container["cpu_limit"]
    try:
        if cpu_limit <= 0:
            problems.append(f"{container_id} cpu limit is below zero")
    except TypeError:
        problems.append(f"Cpu limit is invalid type. Got: {type(cpu_limit).__name__}")
    
    memory_limit = container["memory_limit"]
    if not isinstance(memory_limit, str):
        problems.append(f"{container_id} memory limit is invalid type: must be a string")

    else:
        if memory_limit.endswith(ALLOWED_MEMORY_SUFFIXES):
            memory_limit_str = memory_limit[:-2]
            try:
                if int(memory_limit_str) <= 0:
                    problems.append(f"{container_id} memory limit is invalid")
            except ValueError:
                 problems.append(
                    f"Container {container_id}: invalid memory_limit '{memory_limit}'"
                )
        else:
            problems.append(f"{container_id} memory limit is invalid")

    return problems



def audit_deployments(containers: list[dict]) -> dict:
    results = {
        "audit_passed": False,
        "environement": None,
        "total_containers": 0,
        "valid_containers": 0,
        "invalid_containers": 0,
        "flagged_containers": [],
        "reasons": []
    }

    if not isinstance(containers, list):
        results["reasons"].append(f"Containers is not a list")
        return results

    results["total_containers"] = len(containers)
    environments = set()

    for container in containers:
        if not isinstance(container, dict):
            results["invalid_containers"] += 1
            results["flagged_containers"].append("<unknown>")
            results["reasons"].append(f"Container must be a dictionary")
            continue

        container_id = container.get("container_id", "<unknown>")
        environment = container.get("environment", None)
        if environment is not None:
            environments.add(environment)

        problems = validate_container(container)
        if problems:
            results["invalid_containers"] += 1
            results["flagged_containers"].append(container_id)
            results["reasons"].extend(problems)
        else:
            results["valid_containers"] += 1
  
    if len(environments) == 1:
        results["environement"] = next(iter(environments))

    if len(environments) > 1:
        results["reasons"].append(f"Invalid: Belongs to multiple environments")
    
    if results["environement"] != "production":
        results["reasons"].append(f"Environment must be 'production'")
    
    if (
        results["invalid_containers"] == 0
        and len(environments) == 1
        and results["envrionment"] == "production"
    ):
        results["audit_passed"] = True
    
    return results


if __name__ == "__main__":
    file_path = "container_deployments.json"
    try:
        with open(file_path, 'r') as file:
            containers = json.load(file)
    except FileNotFoundError:
        print(f"The file {file_path} can't be found or does not exist")
    except json.JSONDecodeError as err:
        print(f"The file is invalid JSON: {err}")

result = audit_deployments(containers)
print(json.dumps(result, indent=4))