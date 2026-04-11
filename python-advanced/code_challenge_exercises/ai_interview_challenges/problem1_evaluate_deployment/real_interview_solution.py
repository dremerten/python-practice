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
    "last_checkin_minutes_ago"
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

    if not isinstance(host["disk_usage_percent"], (int, float)):
        problems.append(f"Host {hostname} disk usage percent is invalid")
    elif host["disk_usage_percent"] >= 90:
        problems.append(f"Host {hostname} has exceeded the disk usage limit. Currently at {host["disk_usage_percent"]}")

    if not isinstance(host["cpu_load_percent"], (int, float)):
        problems.append(
            f"Host {hostname} cpu load percent is invalid"
            )
    elif host["cpu_load_percent"] > 85:
        problems.append(
            f"Host {hostname} has exceed the max cpu load percentage. Currently at {host["cpu_load_percent"]}"
            )
    
    if not isinstance(host["memory_usage_percent"], (int, float)):
        problems.append(
            f"Host {hostname} memory usage is invalid."
        )
    elif host["memory_usage_percent"] > 90:
        problems.append(
            f"Host {hostname} has exceeded max memory usage limit. Currently at {host["memory_usage_percent"]} "
        )
    
    if not isinstance(host["agent_version"], str):
        problems.append(
            f"Host {hostname} agent version must be a string. Got {type(host["agent_version"]).__name__}"
            )
    elif host["agent_version"] != REQUIRED_AGENT_VERSION:
        problems.append(
            f"Host {hostname} not running version: {REQUIRED_AGENT_VERSION}!"
            )
    
    if not isinstance(host["last_checkin_minutes_ago"], (int, float)):
        problems.append(
            f"Host {hostname} last_checkin_minutes_ago must be an int or fload"
        )
    elif host["last_checkin_minutes_ago"] > 5:
        problems.append(
            f"Host {hostname} has exceeded 5 minute threshold to check-in"
        )
    
    return problems


def evaluate_deployment(host_reports: list) -> dict:
    results = {
        "deployment_allowed": False,
        "environment": None,
        "total_hosts": 0,
        "healthy_hosts": 0,
        "unhealthy_hosts": 0,
        "failed_hosts": [],
        "reasons": []
    }

    if not isinstance(host_reports, list):
        results["reasons"].append("Host Report must be a list")
        return results

    results["total_hosts"] = len(host_reports)
    environments = set()

    for host in host_reports:
        if not isinstance(host, dict):
            results["unhealthy_hosts"] += 1
            results["failed_hosts"].append("<unknown>")
            results["reasons"].append(f"Host {host} must be a dictionary")
            continue

        hostname = host.get("hostname", "<unknown>")
        environment = host.get("environment")
        if environment is not None:
            environments.add(environment)

        problems = validate_host(host)
        if problems:
            results["unhealthy_hosts"] += 1
            results["failed_hosts"].append(hostname)
            results["reasons"].extend(problems)
        else:
            results["healthy_hosts"] += 1  

    if len(environments) == 1:
        results["environment"] = next(iter(environments))
    elif len(environments) > 1:
        results["reasons"].append("Hosts belong to multiple environments")

    if results["total_hosts"] < 3:
        results["reasons"].append(f"Total Hosts must be greater that 3")
    
    if results["environment"] != "production":
        results["reasons"].append(
            f"Deployment environment must be production"
            )
    
    if (
        results["total_hosts"] >= 3
        and results["unhealthy_hosts"] == 0
        and len(environments) == 1
        and results["environment"] == 'production' 
    ):
        results["deployment_allowed"] = True


    return results
            
        
if __name__ == "__main__":
    host_reports = "host_reports.json"
    try:
        with open(host_reports, 'r') as file:
            host_reports = json.load(file)
    except FileNotFoundError:
        print(f"The file {host_reports} can't be found or does not exits")
    except json.JSONDecodeError:
        print(f"{host_reports} is invalid JSON")
    
    result = evaluate_deployment(host_reports)
    print(json.dumps(result, indent=4))
