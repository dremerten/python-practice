"""
INTERVIEW CHALLENGE: BACKUP RECOVERY READINESS EVALUATION

Implement exactly:
- validate_backup_job(job: dict) -> list[str]
- evaluate_recovery_readiness(backup_jobs: list[dict]) -> dict

Also include these imports:
- import pprint
- import json

Do NOT change:
- constant names
- required keys
- threshold values
- allowed backup target values
- error message text
- return structure
- field names

======================================================================
1) CONSTANTS
======================================================================

[ ] Define a constant set named REQUIRED_KEYS containing exactly these keys:
    - job_name
    - environment
    - enabled
    - last_success_hours_ago
    - retention_days
    - encrypted
    - restore_tested
    - backup_target

======================================================================
2) FUNCTION: validate_backup_job(job)
======================================================================

GOAL
[ ] Validate one backup job
[ ] Return a list of problems
[ ] Return an empty list if the backup job is valid

SETUP
[ ] Create a variable named problems
[ ] problems must start as an empty list

INPUT VALIDATION
[ ] Check whether job is a dictionary
[ ] If job is not a dictionary:
    [ ] Return EXACTLY:
        ["Invalid backup job: not a dictionary"]

JOB NAME
[ ] Read job_name from job
[ ] If job_name is missing, use "<unknown>" as default value

REQUIRED KEYS
[ ] Create a variable named missing_keys
[ ] missing_keys must be computed as REQUIRED_KEYS - job.keys()

[ ] If missing_keys is not empty:
    [ ] Append EXACTLY this string to problems:

        f"Job {job_name} is missing required keys: {sorted(missing_keys)}"

    [ ] Return problems immediately

----------------------------------------------------------------------
VALIDATIONS
Run the following checks in this exact order.
All messages in this section must be appended to problems.
----------------------------------------------------------------------

ENABLED
[ ] Evaluate job["enabled"]

[ ] If job["enabled"] is not True:
    [ ] Append EXACTLY this string:

        f"{job_name} is not enabled"

LAST SUCCESS AGE
[ ] Use a try/except TypeError block when evaluating job["last_success_hours_ago"]

[ ] Inside the try block:
    [ ] Assign job["last_success_hours_ago"] to a variable named last_success_hours_ago
    [ ] Evaluate whether last_success_hours_ago is greater than 24

[ ] If last_success_hours_ago is greater than 24:
    [ ] Append EXACTLY this string:

        f"{job_name} last success is older than 24 hours"

[ ] Inside the except TypeError block:
    [ ] Append EXACTLY this string:

        f"{job_name} has invalid last_success_hours_ago value"

RETENTION
[ ] Use a try/except TypeError block when evaluating job["retention_days"]

[ ] Inside the try block:
    [ ] Assign job["retention_days"] to a variable named retention_days
    [ ] Evaluate whether retention_days is less than 30

[ ] If retention_days is less than 30:
    [ ] Append EXACTLY this string:

        f"{job_name} retention is less than 30 days"

[ ] Inside the except TypeError block:
    [ ] Append EXACTLY this string:

        f"{job_name} has invalid retention_days value"

ENCRYPTION
[ ] Assign job["encrypted"] to a variable named encrypted

[ ] If encrypted is not True:
    [ ] Append EXACTLY this string:

        f"{job_name} is not encrypted."

RESTORE TEST
[ ] Assign job["restore_tested"] to a variable named restore_tested

[ ] If restore_tested is not True:
    [ ] Append EXACTLY this string:

        f"{job_name} has not been restore-tested"

BACKUP TARGET
[ ] Evaluate job["backup_target"]

[ ] If job["backup_target"] is not one of:
    [ ] "s3"
    [ ] "gcs"
    [ ] "azure_blob"

[ ] Append EXACTLY this string:

        f"{job_name} has invalid backup target: {job['backup_target']}"

RETURN VALUE
[ ] Return problems

======================================================================
3) FUNCTION: evaluate_recovery_readiness(backup_jobs)
======================================================================

GOAL
[ ] Validate all backup jobs
[ ] Aggregate findings
[ ] Decide whether recovery readiness is allowed

RESULT STRUCTURE
[ ] Create a variable named result
[ ] result must start as EXACTLY:

    {
        "recovery_ready": False,
        "environment": None,
        "total_jobs": 0,
        "healthy_jobs_count": 0,
        "failed_jobs_count": 0,
        "failed_jobs": [],
        "reasons": [],
    }

INPUT VALIDATION
[ ] Check whether backup_jobs is a list

[ ] If backup_jobs is not a list:
    [ ] Append EXACTLY this string to result["reasons"]:

        f"Must be a list, got: {type(backup_jobs).__name__}"

    [ ] Return result immediately

INITIAL METRICS
[ ] Set result["total_jobs"] to len(backup_jobs)

[ ] Create a variable named environments
[ ] environments must start as an empty set

LOOP THROUGH JOBS
[ ] Process each job in backup_jobs

FOR INVALID JOB ENTRIES
[ ] If a job entry is not a dictionary:
    [ ] Increment result["failed_jobs_count"] by 1
    [ ] Append EXACTLY this string to result["failed_jobs"]:
        "<unknown>"
    [ ] Append EXACTLY this string to result["reasons"]:
        "Invalid backup job: not a dictionary"
    [ ] Continue to the next job

FOR VALID JOB ENTRIES
[ ] Read job_name from the job
[ ] If job_name is missing, use "<unknown>"

[ ] Read environment from the job

[ ] If environment is not None:
    [ ] Add environment to the environments set

JOB VALIDATION
[ ] Call validate_backup_job(job)
[ ] Store the returned list in a variable named problems

CLASSIFICATION
[ ] If problems is not empty:
    [ ] Increment result["failed_jobs_count"] by 1
    [ ] Append job_name to result["failed_jobs"]
    [ ] Extend result["reasons"] with all strings from problems

[ ] Otherwise:
    [ ] Increment result["healthy_jobs_count"] by 1

----------------------------------------------------------------------
POST-PROCESSING RULES
All messages in this section must be added to result["reasons"].
----------------------------------------------------------------------

ENVIRONMENT CONSISTENCY
[ ] If len(environments) == 1:
    [ ] Set result["environment"] to next(iter(environments))

[ ] Elif len(environments) > 1:
    [ ] Append EXACTLY this string to result["reasons"]:

        "Backup jobs belong to multiple environments"

MINIMUM JOB COUNT
[ ] If result["total_jobs"] is less than 5:
    [ ] Append EXACTLY this string to result["reasons"]:

        "Total jobs are less than 5"

ENVIRONMENT REQUIREMENT
[ ] If result["environment"] != "production":
    [ ] Append EXACTLY this string to result["reasons"]:

        "Environment is not 'production'"

FINAL DECISION
[ ] Set result["recovery_ready"] to True only if ALL of the following are true:
    [ ] result["total_jobs"] is at least 5
    [ ] result["failed_jobs_count"] is 0
    [ ] len(environments) == 1
    [ ] result["environment"] == "production"

RETURN VALUE
[ ] Return result

======================================================================
4) MAIN EXECUTION BLOCK
======================================================================

[ ] Add this exact main guard:

    if __name__ == "__main__":

[ ] Define a constant named PATH with this exact value:
    "backup_jobs.json"

[ ] Inside the main block, use a try block

[ ] Open PATH in read mode using:
    with open(PATH, 'r') as f:

[ ] Load the JSON contents into a variable named backup_jobs using json.load(f)

[ ] Call evaluate_recovery_readiness(backup_jobs)
[ ] Store the returned value in a variable named result

[ ] Print the result using:
    pprint.pprint(result, indent=4)

EXCEPTIONS
[ ] Add an except json.JSONDecodeError block
[ ] Print EXACTLY:
    "File is invalid JSON"

[ ] Add an except FileNotFoundError block
[ ] Print EXACTLY:
    f"The config file: {PATH} does not exist or can't be found"

======================================================================
EXPECTED RESULTS
Using this backup_jobs.json input:
======================================================================
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
"""