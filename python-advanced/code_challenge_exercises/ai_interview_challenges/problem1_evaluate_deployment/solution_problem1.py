import pprint
import json

REQUIRED_AGENT_VERSION = "3.2.1"

REQUIRED_KEYS = {
    "hostname",
    "environment",
    "reachable",
    "disk_usage_percent",
    "cpu_load_percent",
    "memory_usage_percent",
    "agent_version",
    "last_checkin_minutes_ago",
}


def validate_host(host: dict) -> list[str]:
    problems = []

    if not isinstance(host, dict):
        return ["Invalid host: not a dictionary"]

    hostname = host.get("hostname", "<unknown>")

    missing_keys = [key for key in REQUIRED_KEYS if key not in host]
    if missing_keys:
        problems.append(f"Host {hostname} is missing required keys. Missing {missing_keys}")
        return problems

    if host["reachable"] is not True:
        problems.append(f"Host {hostname} is offline")

    try:
        if host["disk_usage_percent"] >= 90:
            problems.append(
                f"Host {hostname} has exceeded max disk usage percent limit. Currently at {host['disk_usage_percent']}"
            )
    except TypeError:
        problems.append(f"Host {hostname} disk usage percent is invalid")

    try:
        if host["cpu_load_percent"] > 85:
            problems.append(
                f"Host {hostname} has exceeded max cpu load percent limit. Currently at {host['cpu_load_percent']}"
            )
    except TypeError:
        problems.append(f"Host {hostname} cpu load percent is invalid")

    try:
        if host["memory_usage_percent"] > 90:
            problems.append(
                f"Host {hostname} has exceeded max memory usage limit. Currently at {host['memory_usage_percent']}"
            )
    except TypeError:
        problems.append(f"Host {hostname} memory usage percent is invalid")

    if host["agent_version"] != REQUIRED_AGENT_VERSION:
        problems.append(
            f"Host {hostname} is not running the correct agent version. {REQUIRED_AGENT_VERSION} is required"
        )

    try:
        if host["last_checkin_minutes_ago"] > 5:
            problems.append(
                f"Host {hostname} has exceeded max checkin period of 5mins. Currently at {host['last_checkin_minutes_ago']}"
            )
    except TypeError:
        problems.append(f"Host {hostname} last checkin is invalid")

    return problems


def evaluate_deployment(host_reports: list[dict]) -> dict:
    result = {
        "deployment_allowed": False,
        "environment": None,
        "total_hosts": 0,
        "healthy_hosts": 0,
        "unhealthy_hosts": 0,
        "failed_hosts": [],
        "reasons": [],
    }

    if not isinstance(host_reports, list):
        result["reasons"].append("host report must be a list")
        return result

    result["total_hosts"] = len(host_reports)

    environments = set()

    for host in host_reports:
        if not isinstance(host, dict):
            result["unhealthy_hosts"] += 1
            result["failed_hosts"].append("<unknown>")
            result["reasons"].append("Invalid host: not a dictionary")
            continue

        hostname = host.get("hostname", "<unknown>")
        environment = host.get("environment", None)

        if environment is not None:
            environments.add(environment)

        problems = validate_host(host)

        if problems:
            result["unhealthy_hosts"] += 1
            result["failed_hosts"].append(hostname)
            result["reasons"].extend(problems)
        else:
            result["healthy_hosts"] += 1

    if len(environments) == 1:
        result["environment"] = next(iter(environments))
    elif len(environments) > 1:
        result["reasons"].append("Hosts belong to multiple environments")

    if result["total_hosts"] < 3:
        result["reasons"].append("Total hosts are less than 3")

    if result["environment"] != "production":
        result["reasons"].append("Deployment environment must be production")

    if (
        result["total_hosts"] >= 3
        and result["unhealthy_hosts"] == 0
        and len(environments) == 1
        and result["environment"] == "production"
    ):
        result["deployment_allowed"] = True

    return result


if __name__ == "__main__":
    with open("host_reports.json", "r") as f:
        host_reports = json.load(f)

    pprint.pprint(evaluate_deployment(host_reports), indent=4)

    # To debug validate_host function
    # for host in host_reports:
