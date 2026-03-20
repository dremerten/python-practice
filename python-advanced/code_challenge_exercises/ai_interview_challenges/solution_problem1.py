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

    missing_keys = sorted(REQUIRED_KEYS - set(host.keys()))
    if missing_keys:
        for key in missing_keys:
            problems.append(f"Missing required key: {key}")
        return problems

    hostname = host.get("hostname", "<unknown>")

    if host["reachable"] is not True:
        problems.append(f"Host {hostname} is not reachable")

    try:
        if host["disk_usage_percent"] >= 90:
            problems.append(
                f"Host {hostname} has disk usage {host['disk_usage_percent']}%, must be below 90%"
            )
    except TypeError:
        problems.append(f"Host {hostname} has invalid disk_usage_percent value")

    try:
        if host["cpu_load_percent"] > 85:
            problems.append(
                f"Host {hostname} has CPU load {host['cpu_load_percent']}%, must be 85% or lower"
            )
    except TypeError:
        problems.append(f"Host {hostname} has invalid cpu_load_percent value")

    try:
        if host["memory_usage_percent"] > 90:
            problems.append(
                f"Host {hostname} has memory usage {host['memory_usage_percent']}%, must be 90% or lower"
            )
    except TypeError:
        problems.append(f"Host {hostname} has invalid memory_usage_percent value")

    if host["agent_version"] != REQUIRED_AGENT_VERSION:
        problems.append(
            f"Host {hostname} has agent version {host['agent_version']}, expected {REQUIRED_AGENT_VERSION}"
        )

    try:
        if host["last_checkin_minutes_ago"] > 5:
            problems.append(
                f"Host {hostname} last checked in {host['last_checkin_minutes_ago']} minutes ago, must be 5 or fewer"
            )
    except TypeError:
        problems.append(f"Host {hostname} has invalid last_checkin_minutes_ago value")

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
        result["reasons"].append("Input must be a list of host reports")
        return result

    result["total_hosts"] = len(host_reports)

    if not host_reports:
        result["reasons"].append("No host reports provided")
        return result

    environments = set()

    for index, host in enumerate(host_reports):
        if not isinstance(host, dict):
            result["unhealthy_hosts"] += 1
            result["failed_hosts"].append("<unknown>")
            result["reasons"].append(
                f"Item at index {index} is not a dictionary"
            )
            continue

        hostname = host.get("hostname", "<unknown>")
        environment = host.get("environment")

        if environment is not None:
            environments.add(environment)

        problems = validate_host(host)

        if problems:
            result["unhealthy_hosts"] += 1
            result["failed_hosts"].append(hostname)
            result["reasons"].extend(problems)
        else:
            result["healthy_hosts"] += 1

    if len(host_reports) < 3:
        result["reasons"].append("At least 3 hosts are required for deployment")

    if len(environments) == 1:
        result["environment"] = next(iter(environments))
    elif len(environments) > 1:
        result["reasons"].append("Hosts do not all belong to the same environment")

    if result["environment"] != "production":
        if result["environment"] is None:
            result["reasons"].append("Environment could not be determined")
        else:
            result["reasons"].append(
                f"Deployment environment must be production, got {result['environment']}"
            )

    if result["unhealthy_hosts"] > 0:
        result["reasons"].append("Not all hosts are healthy")

    result["deployment_allowed"] = (
        result["total_hosts"] >= 3
        and result["unhealthy_hosts"] == 0
        and result["environment"] == "production"
        and len(environments) == 1
    )

    return result


if __name__ == "__main__":
    host_reports = [
        {
            "hostname": "web-01",
            "environment": "production",
            "reachable": True,
            "disk_usage_percent": 71,
            "cpu_load_percent": 44,
            "memory_usage_percent": 67,
            "agent_version": "3.2.1",
            "last_checkin_minutes_ago": 1,
        },
        {
            "hostname": "web-02",
            "environment": "production",
            "reachable": True,
            "disk_usage_percent": 82,
            "cpu_load_percent": 65,
            "memory_usage_percent": 73,
            "agent_version": "3.2.1",
            "last_checkin_minutes_ago": 3,
        },
        {
            "hostname": "web-03",
            "environment": "production",
            "reachable": True,
            "disk_usage_percent": 68,
            "cpu_load_percent": 51,
            "memory_usage_percent": 70,
            "agent_version": "3.2.1",
            "last_checkin_minutes_ago": 2,
        },
    ]

    print(evaluate_deployment(host_reports))