import pprint
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
    "memory_limit",
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
        problems.append(
            f"Container {container_id}: missing required keys: {sorted(missing_keys)}"
        )
        return problems

    if container["privileged"] is not False:
        problems.append(f"Container {container_id}: privileged mode must be disabled")

    tag = container["tag"]
    if tag in DISALLOWED_TAGS:
        problems.append(f"Container {container_id}: disallowed tag '{tag}'")

    restart_policy = container["restart_policy"]
    if restart_policy not in ALLOWED_RESTART_POLICIES:
        problems.append(
            f"Container {container_id}: invalid restart policy '{restart_policy}'"
        )

    cpu_limit = container["cpu_limit"]
    try:
        if cpu_limit <= 0:
            problems.append(
                f"Container {container_id}: cpu_limit {cpu_limit} must be greater than 0"
            )
    except TypeError:
        problems.append(
            f"Container {container_id}: invalid cpu_limit value '{cpu_limit}'"
        )

    memory_limit = container["memory_limit"]
    if not isinstance(memory_limit, str):
        problems.append(
            f"Container {container_id}: invalid memory_limit '{memory_limit}'"
        )
    else:
        if memory_limit.endswith(ALLOWED_MEMORY_SUFFIXES):
            numeric_part = memory_limit[:-2]
            try:
                if int(numeric_part) <= 0:
                    problems.append(
                        f"Container {container_id}: invalid memory_limit '{memory_limit}'"
                    )
            except ValueError:
                problems.append(
                    f"Container {container_id}: invalid memory_limit '{memory_limit}'"
                )
        else:
            problems.append(
                f"Container {container_id}: invalid memory_limit '{memory_limit}'"
            )

    return problems


def audit_deployments(containers: list[dict]) -> dict:
    result = {
        "audit_passed": False,
        "environment": None,
        "total_containers": 0,
        "valid_containers": 0,
        "invalid_containers": 0,
        "flagged_containers": [],
        "reasons": [],
    }

    if not isinstance(containers, list):
        result["reasons"].append(
            "Invalid input: containers must be provided as a list"
        )
        return result

    result["total_containers"] = len(containers)
    environments = set()

    for container in containers:
        if not isinstance(container, dict):
            result["invalid_containers"] += 1
            result["flagged_containers"].append("<unknown>")
            result["reasons"].append("Invalid container: not a dictionary")
            continue

        container_id = container.get("container_id", "<unknown>")
        environment = container.get("environment", None)

        if environment is not None:
            environments.add(environment)

        problems = validate_container(container)

        if problems:
            result["invalid_containers"] += 1
            result["flagged_containers"].append(container_id)
            result["reasons"].extend(problems)
        else:
            result["valid_containers"] += 1

    if len(environments) == 1:
        result["environment"] = next(iter(environments))
    elif len(environments) > 1:
        result["reasons"].append("Containers belong to multiple environments")

    if result["environment"] != "production":
        result["reasons"].append("Environment is not production")

    result["audit_passed"] = (
        result["invalid_containers"] == 0
        and len(environments) == 1
        and result["environment"] == "production"
    )

    return result


if __name__ == "__main__":
    try:
        with open("container_deployments.json", "r") as file:
            containers = json.load(file)

        result = audit_deployments(containers)
        pprint.pprint(result)

    except FileNotFoundError:
        print("Error: container_deployments.json file was not found.")
    except json.JSONDecodeError:
        print("Error: container_deployments.json contains invalid JSON.")