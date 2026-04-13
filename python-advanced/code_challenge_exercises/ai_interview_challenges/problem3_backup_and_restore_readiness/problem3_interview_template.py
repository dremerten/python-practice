"""

You are given backup job records and need to determine whether a system is recovery-ready.

Write two functions:

- validate_backup_job(job: dict) -> list[str]
- evaluate_recovery_readiness(backup_jobs: list[dict]) -> dict

Also include:
- import pprint
- import json

Use a constant set named REQUIRED_KEYS with exactly these fields:
- job_name
- environment
- enabled
- last_success_hours_ago
- retention_days
- encrypted
- restore_tested
- backup_target

The goal of validate_backup_job is to inspect one job and return a list of validation failures. 
If the job is fully valid, return an empty list.

The first thing this function should do is validate the input itself. 
If the value passed in is not a dictionary, return exactly:
["Invalid backup job: not a dictionary"]

After that, read job_name from the dictionary, using "<unknown>" if it is missing.

Before checking any individual fields, verify that all required keys are present. 
Compute missing_keys as REQUIRED_KEYS - job.keys(). If any keys are missing, append exactly:
f"Job {job_name} is missing required keys: {sorted(missing_keys)}"
and return immediately. Do not continue validating other fields once required keys are missing.

If all required keys exist, perform the remaining validations in this exact order
 and collect every problem found.

First, check enabled. If job["enabled"] is not True, append:
f"{job_name} is not enabled"

Next, validate last_success_hours_ago. Use a try/except TypeError block. 
Inside the try block, assign job["last_success_hours_ago"] to a variable named last_success_hours_ago, 
then compare it to 24. If it is greater than 24, append:
f"{job_name} last success is older than 24 hours"
If a TypeError happens during that comparison, append:
f"{job_name} has invalid last_success_hours_ago value"

Then validate retention_days the same way, 
also using a try/except TypeError block. Assign job["retention_days"] to a variable named retention_days. 
If retention_days is less than 30, append:
f"{job_name} retention is less than 30 days"
If a TypeError occurs, append:
f"{job_name} has invalid retention_days value"

Then assign job["encrypted"] to a variable named encrypted. If encrypted is not True, append:
f"{job_name} is not encrypted."

Then assign job["restore_tested"] to a variable named restore_tested.
 If restore_tested is not True, append:
f"{job_name} has not been restore-tested"

Finally, validate backup_target. It must be one of:
- "s3"
- "gcs"
- "azure_blob"
If it is not one of those values, append:
f"{job_name} has invalid backup target: {job['backup_target']}"

At the end of validate_backup_job, return the list of problems.

The second function, evaluate_recovery_readiness,
 should validate the full collection and produce a summary result.

Initialize a variable named result exactly as:

{
    "recovery_ready": False,
    "environment": None,
    "total_jobs": 0,
    "healthy_jobs_count": 0,
    "failed_jobs_count": 0,
    "failed_jobs": [],
    "reasons": [],
}

The first check in this function is whether backup_jobs is a list. If it is not, append exactly:
f"Must be a list, got: {type(backup_jobs).__name__}"
to result["reasons"] and return result immediately.

If the input is a list, set result["total_jobs"] to len(backup_jobs),
 and create an empty set named environments.

Then iterate through each job in backup_jobs.

If an entry is not a dictionary, treat it as a failed job immediately.
 Increment result["failed_jobs_count"] by 1, append "<unknown>" to result["failed_jobs"],
append exactly:
"Invalid backup job: not a dictionary"
to result["reasons"], and continue to the next item.

If the entry is a dictionary,
- read job_name with a default of "<unknown>". 
- read environment. 
If environment is not None, 
    add it to the environments set.

Then call validate_backup_job(job) and store the returned list in a variable named problems.

If problems is not empty, this job is failed. 
Increment result["failed_jobs_count"], append job_name to result["failed_jobs"], 
and extend result["reasons"] with every message in problems.

If problems is empty, increment result["healthy_jobs_count"].

After all jobs have been processed, apply the system-level readiness rules.

If there is exactly one unique environment in the environments set,
 set result["environment"] to that single value.

If there is more than one environment, append exactly:
"Backup jobs belong to multiple environments"

If result["total_jobs"] is less than 5, append exactly:
"Total jobs are less than 5"

If result["environment"] is not equal to "production", append exactly:
"Environment is not 'production'"

Set result["recovery_ready"] to True only if all of the following are true:
- result["total_jobs"] is at least 5
- result["failed_jobs_count"] is 0
- len(environments) == 1
- result["environment"] == "production"

Then return result.

Your file must also include a main execution block using this exact guard:

if __name__ == "__main__":

Inside that block, define:
PATH = "backup_jobs.json"

Use a try block. Open the file exactly with:
with open(PATH, 'r') as f:

Load the JSON into a variable named backup_jobs using json.load(f)

Call evaluate_recovery_readiness(backup_jobs), 
store the return value in result, and print it using:
pprint.pprint(result, indent=4)

Also handle these two exceptions exactly:
- except json.JSONDecodeError: print("File is invalid JSON")
- except FileNotFoundError: print(f"The config file: {PATH} does not exist or can't be found")

Expected behavior:
- A valid job returns no problems.
- A job with all required fields but multiple invalid values should return multiple error messages.
- A job missing required fields should stop further validation and return only the missing-keys message.
- The final readiness decision depends on both job-level health and collection-level rules.
- Recovery readiness should remain False if there are any failed jobs,
 fewer than 5 total jobs, multiple environments, or a non-production environment.

For the provided sample data, the final result should be:

{
    "recovery_ready": False,
    "environment": None,
    "total_jobs": 5,
    "healthy_jobs_count": 2,
    "failed_jobs_count": 3,
    "failed_jobs": [
        "redis-snapshot",
        "logs-archive",
        "metrics-backup",
    ],
    "reasons": [
        "redis-snapshot last success is older than 24 hours",
        "redis-snapshot retention is less than 30 days",
        "redis-snapshot has not been restore-tested",
        "logs-archive is not enabled",
        "metrics-backup is not encrypted.",
        "Backup jobs belong to multiple environments",
        "Environment is not 'production'",
    ],
}

A strong implementation should be organized in this order:
- imports
- REQUIRED_KEYS
- validate_backup_job
- evaluate_recovery_readiness
- main block

The important implementation choices are:
- fail immediately only when the input is not a dictionary or required keys are missing
- otherwise collect all validation failures for that job
- separate per-job validation from overall system readiness
- keep all messages, thresholds, field names, and return structure exact
"""