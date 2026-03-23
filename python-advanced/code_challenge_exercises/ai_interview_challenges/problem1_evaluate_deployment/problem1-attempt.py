import pprint

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
    # TODO: initialize problems list
    problems = []

    # TODO: if host is not a dict:
    # - return ["Invalid host: not a dictionary"]
    if not isinstance(host, dict):
        return ["Invalid host: not a dictionary"]

    # TODO: extract hostname with default "<unknown>"
    hostname = host.get("hostname", "<unknown>")

    # TODO: compute missing_keys from REQUIRED_KEYS
    # - if missing_keys:
    #     - append problem message
    #     - return problems
    missing_keys = [key for key in REQUIRED_KEYS if key not in host]
    if missing_keys:
        problems.append(f"Host {hostname} is missing required keys. Missing {missing_keys}")
        return problems

    # TODO: check if host is reachable
    # - if not True:
    #     - append problem
    if host["reachable"] is not True:
        problems.append(f"Host {hostname} is offline")

    # TODO: validate disk_usage_percent
    # - try:
    #     - if >= 90:
    #         - append problem
    # - except TypeError:
    #     - append invalid value problem
    try:
        if host["disk_usage_percent"] >= 90:
            problems.append(f"Host {hostname} has exceeded max disk usage percent limit. Currently at {host['disk_usage_percent']}")
    except TypeError:
        problems.append(f"Host {hostname} disk usage percent is invalid")

    # TODO: validate cpu_load_percent
    # - try:
    #     - if > 85:
    #         - append problem
    # - except TypeError:
    #     - append invalid value problem
    try:
        if host["cpu_load_percent"] > 85:
            problems.append(f"Host {hostname} has exceeded max cpu load percent limit. Currently at {host['cpu_load_percent']}")
    except TypeError:
        problems.append(f"Host {hostname} cpu load percent is invalid")

    # TODO: validate memory_usage_percent
    # - try:
    #     - if > 90:
    #         - append problem
    # - except TypeError:
    #     - append invalid value problem
    try:
        if host["memory_usage_percent"] > 90:
            problems.append(f"Host {hostname} has exceeded max memory usage limit. Currently at {host['memory_usage_percent']}")
    except TypeError:
        problems.append(f"Host {hostname} memory usage percent is invalid")
            

    # TODO: validate agent_version
    # - if not equal REQUIRED_AGENT_VERSION:
    #     - append problem
    if host["agent_version"] != REQUIRED_AGENT_VERSION:
        problems.append(f"Host {hostname} is not running the correct agent version. {REQUIRED_AGENT_VERSION} is required")

    # TODO: validate last_checkin_minutes_ago
    # - try:
    #     - if > 5:
    #         - append problem
    # - except TypeError:
    #     - append invalid value problem
    try:
        if host["last_checkin_minutes_ago"] > 5:
            problems.append(f"Host {hostname} has exceeded max checkin period of 5mins. Currently at {host["last_checkin_minutes_ago"]}")
    except TypeError:
        problems.append(f"Host {hostname} last checkin is invalid")

    # TODO: return problems
    return problems


def evaluate_deployment(host_reports: list[dict]) -> dict:
    # TODO: initialize result dictionary with default values
    result = {
    "deployment_allowed": False,
    "environment": None,
    "total_hosts": 0,
    "healthy_hosts": 0,
    "unhealthy_hosts": 0,
    "failed_hosts": [],
    "reasons": [],
    }

    # TODO: if host_reports is not a list:
    # - append reason
    # - return result
    if not isinstance(host_reports, list):
        result["reasons"].append("host report must be a list")
        return result

    # TODO: set result["total_hosts"] to the number of hosts
    result["total_hosts"] = len(host_reports)

    # TODO: initialize environments set
    environments = set()

    # TODO: iterate through host_reports
    # - if host is not a dict:
    #     - increment unhealthy_hosts
    #     - append "<unknown>" to failed_hosts
    #     - append reason "Invalid host: not a dictionary"
    #     - continue
    for host in host_reports:
        if not isinstance(host, dict):
            result["unhealthy_hosts"] += 1
            result["failed_hosts"].append("<unknown>")
            result["reasons"].append("Invalid host: not a dictionary")
            continue

        # - extract hostname with default "<unknown>"
        # - extract environment
        hostname = host.get("hostname", "<unknown>")
        environment = host.get("environment", None)

        # - if environment is not None:
        #     - add to environments set
        if environment is not None:
            environments.add(environment)

        # - call validate_host(host) assign to problems variable
        problems = validate_host(host)

        # - if problems exist:
        #     - increment unhealthy_hosts
        #     - append hostname to failed_hosts
        #     - extend reasons with problems
        # - else:
        #     - increment healthy_hosts
        if problems:
            result["unhealthy_hosts"] +=1
            result["failed_hosts"].append(hostname)
            result["reasons"].extend(problems)
        else:
            result["healthy_hosts"] +=1

    # TODO: evaluate environments
    # - if len(environments) == 1:
    #     - set result["environment"] = next(iter(environments))
    # - elif len(environments) > 1:
    #     - append reason "Hosts belong to multiple environments"
    if len(environments) == 1:
            result["environment"] = next(iter(environments))
    elif len(environments) > 1:
        result["reasons"].append("Hosts belong to multiple environments")

    # TODO: check total_hosts < 3
    # - append reason if true
    if result["total_hosts"] < 3:
        result["reasons"].append("Total hosts are less than 3")

    # TODO: check environment != "production"
    # - append reason if true
    if result["environment"] != "production":
        result["reasons"].append("Deployment environment must be production")

    # TODO: final deployment decision
    # - if total_hosts >= 3
    #   and unhealthy_hosts == 0
    #   and len(environments) == 1
    #   and result["environment"] == "production":
    #     - set result["deployment_allowed"] = True
    if (
        result["total_hosts"] >= 3
        and result["unhealthy_hosts"] == 0
        and len(environments) == 1
        and result["environment"] == "production"
    ):
        result["deployment_allowed"] = True

    return result


if __name__ == "__main__":
    host_reports = [
    {
        "hostname": "web-01",
        "environment": "production",
        "reachable": True,
        "disk_usage_percent": 70,
        "cpu_load_percent": 50,
        "memory_usage_percent": 60,
        "agent_version": "3.2.1",
        "last_checkin_minutes_ago": 1,
    },
    {
        "hostname": "web-02",
        "environment": "production",
        "reachable": True,
        "disk_usage_percent": 65,
        "cpu_load_percent": 45,
        "memory_usage_percent": 55,
        "agent_version": "3.2.1",
        "last_checkin_minutes_ago": 2,
    },
    {
        "hostname": "web-03",
        "environment": "production",
        "reachable": True,
        "disk_usage_percent": 60,
        "cpu_load_percent": 40,
        "memory_usage_percent": 50,
        "agent_version": "3.2.1",
        "last_checkin_minutes_ago": 3,
    },
    {
        "hostname": "web-04",
        "environment": "production",
        "reachable": False,  # unreachable
        "disk_usage_percent": 50,
        "cpu_load_percent": 30,
        "memory_usage_percent": 40,
        "agent_version": "3.2.1",
        "last_checkin_minutes_ago": 1,
    },
    {
        "hostname": "web-05",
        "environment": "production",
        "reachable": True,
        "disk_usage_percent": 95,  # high disk
        "cpu_load_percent": 40,
        "memory_usage_percent": 50,
        "agent_version": "3.2.1",
        "last_checkin_minutes_ago": 1,
    },
    {
        "hostname": "web-06",
        "environment": "production",
        "reachable": True,
        "disk_usage_percent": 60,
        "cpu_load_percent": 90,  # high CPU
        "memory_usage_percent": 50,
        "agent_version": "3.2.1",
        "last_checkin_minutes_ago": 1,
    },
    {
        "hostname": "web-07",
        "environment": "production",
        "reachable": True,
        "disk_usage_percent": 60,
        "cpu_load_percent": 40,
        "memory_usage_percent": 95,  # high memory
        "agent_version": "3.2.1",
        "last_checkin_minutes_ago": 1,
    },
    {
        "hostname": "web-08",
        "environment": "production",
        "reachable": True,
        "disk_usage_percent": 60,
        "cpu_load_percent": 40,
        "memory_usage_percent": 50,
        "agent_version": "3.1.0",  # wrong version
        "last_checkin_minutes_ago": 1,
    },
    {
        "hostname": "web-09",
        "environment": "production",
        "reachable": True,
        "disk_usage_percent": 60,
        "cpu_load_percent": 40,
        "memory_usage_percent": 50,
        "agent_version": "3.2.1",
        "last_checkin_minutes_ago": 10,  # stale
    },
    {
        "hostname": "web-10",
        "environment": "staging",  # wrong environment
        "reachable": True,
        "disk_usage_percent": 60,
        "cpu_load_percent": 40,
        "memory_usage_percent": 50,
        "agent_version": "3.2.1",
        "last_checkin_minutes_ago": 1,
    },
]

    pprint.pprint(evaluate_deployment(host_reports), indent=4)

    # To debug validate_host function
    # for host in host_reports:
    #     print(validate_host(host))