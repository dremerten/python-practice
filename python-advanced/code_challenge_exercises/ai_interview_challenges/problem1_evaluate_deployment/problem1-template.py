"""
This script evaluates whether a group of hosts is ready for deployment.
Each host is validated for health based on connectivity, resource usage, and configuration.
The deployment is only allowed if all hosts are healthy, belong to the same environment,
and meet minimum deployment requirements.

  result = {
        "deployment_allowed": False,
        "environment": None,
        "total_hosts": 0,
        "healthy_hosts": 0,
        "unhealthy_hosts": 0,
        "failed_hosts": [],
        "reasons": [],
    }

"""

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
    # TODO: initialize problems list
    problems = []

    # TODO: if host is not a dict:
    # - return ["Invalid host: not a dictionary"]

    # TODO: extract hostname with default "<unknown>"

    # TODO: compute missing_keys from REQUIRED_KEYS
    # - if missing_keys:
    #     - append problem message
    #     - return problems

    # TODO: check if host is reachable
    # - if not True:
    #     - append problem

    # TODO: validate disk_usage_percent
    # - try:
    #     - if >= 90:
    #         - append problem
    # - except TypeError:
    #     - append invalid value problem

    # TODO: validate cpu_load_percent
    # - try:
    #     - if > 85:
    #         - append problem
    # - except TypeError:
    #     - append invalid value problem

    # TODO: validate memory_usage_percent
    # - try:
    #     - if > 90:
    #         - append problem
    # - except TypeError:
    #     - append invalid value problem

    # TODO: validate agent_version
    # - if not equal REQUIRED_AGENT_VERSION:
    #     - append problem

    # TODO: validate last_checkin_minutes_ago
    # - try:
    #     - if > 5:
    #         - append problem
    # - except TypeError:
    #     - append invalid value problem

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

    # TODO: set result["total_hosts"] to the number of hosts

    # TODO: initialize environments set

    # TODO: iterate through host_reports
    # - if host is not a dict:
    #     - increment unhealthy_hosts
    #     - append "<unknown>" to failed_hosts
    #     - append reason "Invalid host: not a dictionary"
    #     - continue

        # - extract hostname with default "<unknown>"
        # - extract environment

        # - if environment is not None:
        #     - add to environments set

        # - call validate_host(host) assign to problems variable

        # - if problems exist:
        #     - increment unhealthy_hosts
        #     - append hostname to failed_hosts
        #     - extend reasons with problems
        # - else:
        #     - increment healthy_hosts

    # TODO: evaluate environments
    # - if len(environments) == 1:
    #     - set result["environment"] = next(iter(environments))
    # - elif len(environments) > 1:
    #     - append reason "Hosts belong to multiple environments"

    # TODO: check total_hosts < 3
    # - append reason if true

    # TODO: check environment != "production"
    # - append reason if true

    # TODO: final deployment decision
    # - if total_hosts >= 3
    #   and unhealthy_hosts == 0
    #   and len(environments) == 1
    #   and result["environment"] == "production":
    #     - set result["deployment_allowed"] = True

    # TODO: return result
    return result


if __name__ == "__main__":
    # TODO: open "host_reports.json" file
    # - load JSON data into host_reports
    with open("host_reports.json", "r") as f:
        host_reports = json.load(f)

    pprint.pprint(evaluate_deployment(host_reports), indent=4)

    # To debug validate_host function
    # for host in host_reports:
    #     print(validate_host(host))