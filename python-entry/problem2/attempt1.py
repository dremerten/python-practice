import json
import pprint

def analyze_pipeline(path: str) -> dict:
    try:
        with open(path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"The config file can't be found or does not exist: {path}") from e
    except json.JSONDecodeError as e:
        raise ValueError(f"The config file is invalid JSON: {path}") from e
    if isinstance(data, dict):
        jobs = data.get("jobs")
    elif isinstance(data, list):
        jobs = data
    else:
        raise TypeError(f"The config must be a dictionary or list. Instead got: {type(data).__name__}")
    if not isinstance(jobs, list):
        raise TypeError(f"'jobs must be a list. Instead got: {type(jobs).__name__}")
    
    total_duration =  0
    successful_jobs = []
    failed_jobs = []
    pending_jobs = []
    skipped_jobs = []
    unknown_job_status = []
    # pipline_failed = len(failed_jobs) > 0

    for job in jobs:
        if not isinstance(job, dict):
            continue
        name = job.get("name", "<unknown>")
        status = job.get("status")
        duration = job.get("duration", 0)

        if isinstance(duration, int):
            total_duration += duration
        
        if status == "failed":
            failed_jobs.append(name)
        elif status == "success":
            successful_jobs.append(name)
        elif status == "pending":
            pending_jobs.append(name)
        elif status == "skipped":
            skipped_jobs.append(name)
        else:
            unknown_job_status.append(name)
    
    return {
        "Total_duration": total_duration,
        "Successful_jobs": successful_jobs,
        "Failed_jobs": failed_jobs,
        "Pending_jobs": pending_jobs,
        "Skipped_jobs": skipped_jobs,
        "Unknown_jobs" : unknown_job_status,
        "Pipelines_Failed": len(failed_jobs) > 0
    }

if __name__ == "__main__":
    data = analyze_pipeline("/home/andre/DevOps-Practice/python-practice/problem2/pipeline-large.json")
    pprint.pprint(data, indent=4)


