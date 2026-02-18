import json
import sys


def analyze_pipeline(path: str) -> dict:
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError as e:
        raise FileNotFoundError(
            f"Pipeline file not found: {path}"
        ) from e
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Pipeline file contains invalid JSON: {path}"
        ) from e

    if not isinstance(data, dict):
        raise TypeError(
            f"Pipeline root must be a dict, got: {type(data).__name__}"
        )

    jobs = data.get("jobs")
    if not isinstance(jobs, list):
        raise TypeError(
            f"'jobs' must be a list, got: {type(jobs).__name__}"
        )

    total_duration = 0
    successful_jobs = []
    failed_jobs = []
    pending_jobs = []
    skipped_jobs = []
    unknown_status_jobs = []

    for job in jobs:
        if not isinstance(job, dict):
            continue

        name = job.get("name", "<unknown>")
        status = job.get("status")
        duration = job.get("duration", 0)

        if isinstance(duration, int):
            total_duration += duration

        if status == "success":
            successful_jobs.append(name)
        elif status == "failed":
            failed_jobs.append(name)
        elif status == "pending":
            pending_jobs.append(name)
        elif status == "skipped":
            skipped_jobs.append(name)
        else:
            unknown_status_jobs.append(name)

    return {
        "total_duration": total_duration,
        "successful_jobs": successful_jobs,
        "failed_jobs": failed_jobs,
        "pending_jobs": pending_jobs,
        "skipped_jobs": skipped_jobs,
        "unknown_status_jobs": unknown_status_jobs,
        "pipeline_failed": len(failed_jobs) > 0,
    }


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "pipeline.json"
    result = analyze_pipeline(path)
    print(json.dumps(result, indent=2))
