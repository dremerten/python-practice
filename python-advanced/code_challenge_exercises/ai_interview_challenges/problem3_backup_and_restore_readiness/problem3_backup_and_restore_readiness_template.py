"""
This script loads backup job data from a JSON file and evaluates whether
the disaster recovery posture is acceptable. Each backup job must meet
freshness, encryption, and restore-test requirements. Recovery readiness
is only allowed if all backup jobs pass validation and the environment-level
rules are satisfied.
"""

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
    "backup_target",
}


def validate_backup_job(job: dict) -> list[str]:
    # TODO: initialize problems list
    problems = []

    # TODO: if job is not a dict:
    # - return ["Invalid backup job: not a dictionary"]

    # TODO: extract job_name with default "<unknown>"

    # TODO: compute missing_keys from REQUIRED_KEYS
    # - if missing_keys:
    #     - append problem message
    #     - return problems

    # TODO: check if backup job is enabled
    # - if not True:
    #     - append problem

    # TODO: validate last_success_hours_ago
    # - try:
    #     - if > 24:
    #         - append problem
    # - except TypeError:
    #     - append invalid value problem

    # TODO: validate retention_days
    # - try:
    #     - if < 30:
    #         - append problem
    # - except TypeError:
    #     - append invalid value problem

    # TODO: check encryption
    # - if not True:
    #     - append problem

    # TODO: check restore testing
    # - if not True:
    #     - append problem

    # TODO: validate backup_target
    # - if backup_target is not one of:
    #     - "s3"
    #     - "gcs"
    #     - "azure_blob"
    #     - append problem

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

    # TODO: set result["total_jobs"] to the number of backup jobs

    # TODO: initialize environments set

    # TODO: iterate through backup_jobs
    # - if job is not a dict:
    #     - increment failed_jobs_count
    #     - append "<unknown>" to failed_jobs
    #     - append reason "Invalid backup job: not a dictionary"
    #     - continue

        # - extract job_name with default "<unknown>"
        # - extract environment

        # - if environment is not None:
        #     - add to environments set

        # - call validate_backup_job(job) assign to problems variable

        # - if problems exist:
        #     - increment failed_jobs_count
        #     - append job_name to failed_jobs
        #     - extend reasons with problems
        # - else:
        #     - increment healthy_jobs_count

    # TODO: evaluate environments
    # - if len(environments) == 1:
    #     - set result["environment"] = next(iter(environments))
    # - elif len(environments) > 1:
    #     - append reason "Backup jobs belong to multiple environments"

    # TODO: check total_jobs < 5
    # - append reason if true

    # TODO: check environment != "production"
    # - append reason if true

    # TODO: final recovery readiness decision
    # - if total_jobs >= 5
    #   and failed_jobs_count == 0
    #   and len(environments) == 1
    #   and result["environment"] == "production":
    #     - set result["recovery_ready"] = True

    # TODO: return result
    return result


if __name__ == "__main__":
    # TODO: open "backup_jobs.json" file
    # - load JSON data into backup_jobs

    # TODO: call evaluate_recovery_readiness(backup_jobs)

    # TODO: pretty print result using pprint
    pass