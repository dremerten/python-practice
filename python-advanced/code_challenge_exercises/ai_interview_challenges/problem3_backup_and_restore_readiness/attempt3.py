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
        problems.append(
            f"Job: {job_name} is missing required keys: {sorted(missing_keys)}"
            )
        return problems
    
    if job["enabled"] is not True:
        problems.append(f"Job: {job_name} is not enabled")
    
    if not isinstance(job["last_success_hours_ago"], (int, float)) or isinstance(job["last_success_hours_ago"], bool):
        problems.append(f"Job: {job_name} has invalid last_success_hours_ago value")
    elif job["last_success_hours_ago"] > 24:
        problems.append(f"Job: {job_name} last success is older than 24 hours. Got {job["last_success_hours_ago"]} hours")

    if not isinstance(job["retention_days"], (int, float)) or isinstance(job["retention_days"], bool):
        problems.append(f"Job: {job_name} has invalid retention_days value")
    elif job["retention_days"] < 30:
        problems.append(f"Job: {job_name} last success is less than 30 days. Got {job["retention_days"]} days")
    
    encrypted = job["encrypted"]
    if encrypted is not True:
        problems.append(f"Job: {job_name} is not encrypted.")
    
    restore_tested = job["restore_tested"]
    if restore_tested is not True:
        problems.append(f"Job: {job_name} has not been restore-tested")

    backup_target = job.get("backup_target")
    if backup_target not in {"s3", "gcs", "azure_blob"}:
        problems.append(f"{job_name} has invalid backup target: {backup_target}")

    return problems


    
def evaluate_recovery_readiness(backup_jobs: list[dict]) -> dict:
    results = {
    "recovery_ready": False,
    "environment": None,
    "total_jobs": 0,
    "healthy_jobs_count": 0,
    "failed_jobs_count": 0,
    "failed_jobs": [],
    "reasons": [],
    }

    if not isinstance(backup_jobs, list):
        results["reasons"].append(f"Must be a list, got: {type(backup_jobs).__name__}")
        return results
    
    results["total_jobs"] = len(backup_jobs)
    environments = set()

    for job in backup_jobs:
        if not isinstance(job, dict):
            results["failed_jobs_count"] += 1
            results["failed_jobs"].append("<unknown>")
            results["reasons"].append("Invalid backup job: not a dictionary")
            continue
        
        job_name = job.get("job_name", "<unknown>")
        environment = job.get("environment")
        if environment is not None:
            environments.add(environment)
        
        problems = validate_backup_job(job)
        if problems:
            results["failed_jobs_count"] += 1
            results["failed_jobs"].append(job_name)
            results["reasons"].extend(problems)
        else:
            results["healthy_jobs_count"] += 1
    
    if len(environments) == 1:
        result["environment"] = next(iter(environments))
    elif len(environments) > 1:
        results["reasons"].append("Backup jobs belong to multiple environments")
    
    if results["total_jobs"] < 5:
        results["reasons"].append("Total jobs are less than 5")
    
    if results["environment"] != "production":
        results["reasons"].append("Environment is not 'production'")
    
    if (
        results["total_jobs"] >= 5
        and results["failed_jobs_count"] == 0
        and len(environments) == 1
        and results["environment"] == "production"
    ):
        results["recovery_ready"] = True

    return results

if __name__ == "__main__":
    FILE_PATH = "backup_jobs.json"
    try:
        with open(FILE_PATH, 'r') as f:
            backup_jobs = json.load(f)
    except FileNotFoundError:
        print(f"The file {FILE_PATH} can't be found or does not exits")
    except json.JSONDecodeError:
        print(f"The file {backup_jobs} is invalid JSON")
    
results = evaluate_recovery_readiness(backup_jobs)
print("#" * 80)
print("There will be slight differnces in out because I'm using json.dumps to print out")
print("#" * 80)
print(json.dumps(results, indent=4))