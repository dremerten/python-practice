"""
This script loads backup job data from a JSON file and evaluates whether
the disaster recovery posture is acceptable. Each backup job must meet
freshness, encryption, and restore-test requirements. Recovery readiness
is only allowed if all backup jobs pass validation and the environment-level
rules are satisfied.
"""

import pprint
import json

# set()
REQUIRED_KEYS = {
    "job_name",
    "environment",
    "enabled",
    "last_success_hours_ago",
    "retention_days",
    "encrypted",
    "restore_tested",
    "backup_target",
}


def validate_backup_job(job: dict) -> list[str]:
    # TODO: initialize problems list
    problems = []

    # TODO: if job is not a dict:
    # - return ["Invalid backup job: not a dictionary"]
    if not isinstance(job, dict):
        return ["Invalid backup job: not a dictionary"]

    # TODO: extract job_name with default "<unknown>"
    job_name = job.get("job_name", "<unknown>")

    # TODO: compute missing_keys from REQUIRED_KEYS
    # - if missing_keys:
    #     - append problem message
    #     - return problems
    missing_keys = REQUIRED_KEYS - job.keys()
    if missing_keys:
        problems.append(f"Job {job_name} is missing required keys: {sorted(missing_keys)}")
        return problems

    # TODO: check if backup job is enabled
    # - if not True:
    #     - append problem
    if job["enabled"] is not True:
        problems.append(f"{job_name} is not enabled")

    # TODO: validate last_success_hours_ago
    # - try:
    #     - if > 24:
    #         - append problem
    # - except TypeError:
    #     - append invalid value problem
    try:
        last_success_hours_ago = job["last_success_hours_ago"]
        if last_success_hours_ago > 24:
            problems.append(f"{job_name} last success is older than 24 hours")
    except TypeError:
        problems.append(f"{job_name} has invalid last_success_hours_ago value")

    # TODO: validate retention_days
    # - try:
    #     - if < 30:
    #         - append problem
    # - except TypeError:
    #     - append invalid value problem
    try:
        retention_days = job["retention_days"]
        if retention_days < 30:
            problems.append(f"{job_name} retention is less than 30 days")
    except TypeError:
        problems.append(f"{job_name} has invalid retention_days value")

    # TODO: check encryption
    # - if not True:
    #     - append problem
    encrypted = job["encrypted"]
    if encrypted is not True:
        problems.append(f"{job_name} is not encrypted.")

    # TODO: check restore testing
    # - if not True:
    #     - append problem
    restore_tested = job["restore_tested"]
    if restore_tested is not True:
        problems.append(f"{job_name} has not been restore-tested")

    # TODO: validate backup_target
    # - if backup_target is not one of:
    #     - "s3"
    #     - "gcs"
    #     - "azure_blob"
    #     - append problem
    if job["backup_target"] not in {"s3", "gcs", "azure_blob"}:
        problems.append(f"{job_name} has invalid backup target: {job['backup_target']}")

    # TODO: return problems
    return problems


def evaluate_recovery_readiness(backup_jobs: list[dict]) -> dict:
    # TODO: initialize result dictionary with default values
    result = {
    "recovery_ready": False,
    "environment": None,
    "total_jobs": 0,
    "healthy_jobs_count": 0,
    "failed_jobs_count": 0,
    "failed_jobs": [],
    "reasons": [],
    }

    # TODO: if backup_jobs is not a list:
    # - append reason
    # - return result
    if not isinstance(backup_jobs, list):
        result["reasons"].append(f"Must be a list, got: {type(backup_jobs).__name__}")
        return result

    # TODO: set result["total_jobs"] to the number of backup jobs
    result["total_jobs"] = len(backup_jobs)

    # TODO: initialize environments set
    environments = set()

    # TODO: iterate through backup_jobs
    # - if job is not a dict:
    #     - increment failed_jobs_count
    #     - append "<unknown>" to failed_jobs
    #     - append reason "Invalid backup job: not a dictionary"
    #     - continue
    for job in backup_jobs:
        if not isinstance(job, dict):
            result["failed_jobs_count"] += 1
            result["failed_jobs"].append("<unknown>")
            result["reasons"].append(f"Invalid backup job: not a dictionary")
            continue

        # - extract job_name with default "<unknown>"
        # - extract environment
        job_name = job.get("job_name", "<unknown>")
        environment = job.get("environment")

        # - if environment is not None:
        #     - add to environments set
        if environment is not None:
            environments.add(environment)
        # - call validate_backup_job(job) assign to problems variable
        problems = validate_backup_job(job)

        # - if problems exist:
        #     - increment failed_jobs_count
        #     - append job_name to failed_jobs
        #     - extend reasons with problems
        # - else:
        #     - increment healthy_jobs_count
        if problems:
            result["failed_jobs_count"] += 1
            result["failed_jobs"].append(job_name)
            result["reasons"].extend(problems)
        else:
            result["healthy_jobs_count"] += 1

    # TODO: evaluate environments
    # - if len(environments) == 1:
    #     - set result["environment"] = next(iter(environments))
    # - elif len(environments) > 1:
    #     - append reason "Backup jobs belong to multiple environments"
    if len(environments) == 1:
        result["environment"] = next(iter(environments))
    elif len(environments) > 1:
        result["reasons"].append(f"Backup jobs belong to multiple environments")

    # TODO: check total_jobs < 5
    # - append reason if true
    if result["total_jobs"] < 5:
        result["reasons"].append(f"Total jobs are less than 5")

    # TODO: check environment != "production"
    # - append reason if true
    if result["environment"] != "production":
        result["reasons"].append(f"Environment is not 'production'")


    # TODO: final recovery readiness decision
    # - if total_jobs >= 5
    #   and failed_jobs_count == 0
    #   and len(environments) == 1
    #   and result["environment"] == "production":
    #     - set result["recovery_ready"] = True
    if (
        result["total_jobs"] >= 5
        and result["failed_jobs_count"] == 0
        and len(environments) == 1
        and result["environment"] == "production"
        ):
        result["recovery_ready"] = True


    # TODO: return result
    return result


if __name__ == "__main__":
    # TODO: open "backup_jobs.json" file
    # - load JSON data into backup_jobs
    PATH = "backup_jobs.json"
    try:
        with open(PATH, 'r') as f:
            backup_jobs = json.load(f)

    # TODO: call evaluate_recovery_readiness(backup_jobs)
    # TODO: pretty print result using pprint
        result = evaluate_recovery_readiness(backup_jobs)
        pprint.pprint(result, indent=4)
    
    except json.JSONDecodeError:
        print(f"File is invalid JSON")

    except FileNotFoundError:
        print(f"The config file: {PATH} does not exist or can't be found")

