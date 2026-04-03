import pprint
import json

REQUIRED_KEYS = {
    "job_name",
    "environment",
    "enabled",
    "last_success_hours_ago",
    "retention_days",
    "encrypted",
    "restore_tested",
    "backup_target"
}

def validate_backup_job(job: dict) -> list[str]:
    problems = []

    if not isinstance(job, dict):
        return ["Invalid backup job: not a dictionary"]

    job_name = job.get("job_name", "<unknown>")
    missing_keys = REQUIRED_KEYS - job.keys()
    if missing_keys:
        problems.append(f"Job {job_name} is missing required keys: {sorted(missing_keys)}")
        return problems
    
    if job["enabled"] is not True:
        problems.append(f"{job_name} is not enabled")
    
    try:
        last_success_hours_ago = job["last_success_hours_ago"]
        if last_success_hours_ago > 24:
            problems.append(f"{job_name} last success is older than 24 hours")
    except TypeError:
        problems.append(f"{job_name} has invalid last_success_hours_ago value")

    try:
        retention_days = job["retention_days"]
        if retention_days < 30:
            problems.append(f"{job_name} retention is less than 30 days")
    except TypeError:
        problems.append(f"{job_name} has invalid retention_days value")

    encrypted = job["encrypted"]
    if encrypted is not True:
        problems.append(f"{job_name} is not encrypted.")

    restore_tested = job["restore_tested"]
    if restore_tested is not True:
        problems.append(f"{job_name} has not been restore-tested")

    if job["backup_target"] not in {"s3", "gcs", "azure_blob"}:
        problems.append(f"{job_name} has invalid backup target: {job['backup_target']}")
    
    return problems
    


def evaluate_recovery_readiness(backup_jobs: list[dict]) -> dict:
    result =  {
        "recovery_ready": False,
        "environment": None,
        "total_jobs": 0,
        "healthy_jobs_count": 0,
        "failed_jobs_count": 0,
        "failed_jobs": [],
        "reasons": [],
    }

    if not isinstance(backup_jobs, list):
        result["reasons"].append(f"Must be a list, got: {type(backup_jobs).__name__}")
        return result
    
    result["total_jobs"] = len(backup_jobs)
    environments = set()
    for job in backup_jobs:
        if not isinstance(job, dict):
            result["failed_jobs_count"] += 1
            result["failed_jobs"].append("<unknown>")
            result["reasons"].append("Invalid backup job: not a dictionary")
            continue

        job_name = job.get("job_name", "<unknown>")
        environment = job.get("environment", None)
        if environment is not None:
            environments.add(environment)

        problems = validate_backup_job(job)
        if problems:
            result["failed_jobs_count"] += 1
            result["failed_jobs"].append(job_name)
            result["reasons"].extend(problems)
        else:
            result["healthy_jobs_count"] += 1
    
    if len(environments) == 1:
        result["environment"] = next(iter(environments))
    elif len(environments) > 1:
        result["reasons"].append("Backup jobs belong to multiple environments")
    
    if result["total_jobs"] < 5:
        result["reasons"].append("Total jobs are less than 5")
    
    if result["environment"] != "production":
        result["reasons"].append("Environment is not 'production'")
    
    if (
        result["total_jobs"] >= 5
        and result["failed_jobs_count"] == 0
        and len(environments) == 1
        and result["environment"] == "production"
        ):
        result["recovery_ready"] = True
    
    return result


if __name__ == "__main__":
    file_path = "backup_jobs.json"
    try:
        with open(file_path, "r") as f:
            backup_jobs = json.load(f)
            result = evaluate_recovery_readiness(backup_jobs)
            pprint.pprint(result)
    except FileNotFoundError:
        print(f"The file {file_path} cannot be found")
    except json.JSONDecodeError:
        print("The jobs are invalid JSON")
