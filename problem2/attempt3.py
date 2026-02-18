'''
--------------------------------------------------
Your Task
--------------------------------------------------

Write a Python script `pipeline_report.py` that defines:

    def analyze_pipeline(path: str) -> dict:

The script must also support execution as:

    python3 pipeline_report.py pipeline.json

--------------------------------------------------
Requirements
--------------------------------------------------

1. File handling
   1.1 Open the file located at `path`.
   1.2 Raise FileNotFoundError with a clear message if the file does not exist.
   1.3 Raise ValueError with a clear message if the file contains invalid JSON.

2. Input validation
   2.1 Ensure the parsed JSON root object is a dictionary.
   2.2 Raise TypeError if the root object is not a dictionary.
   2.3 Ensure the key "jobs" exists.
   2.4 Ensure "jobs" is a list.
   2.5 Raise TypeError if "jobs" is missing or not a list.

3. Job entry handling
   3.1 Iterate over each item in "jobs".
   3.2 Skip any job entry that is not a dictionary.
   3.3 If "name" is missing, use "<unknown>" as the job name.
   3.4 If "duration" is missing or not an integer, treat it as 0.

4. Metrics calculation
   4.1 Sum the duration of all jobs where "duration" is an integer.
   4.2 Store the total as `total_duration`.

5. Status classification
   5.1 Classify jobs into the following lists based on "status":
       - successful_jobs
       - failed_jobs
       - pending_jobs
       - skipped_jobs
       - unknown_status_jobs
   5.2 Any status other than:
       "success", "failed", "pending", or "skipped"
       must be placed in `unknown_status_jobs`.

6. Pipeline state
   6.1 Set `pipeline_failed` to True if any job has status "failed".
   6.2 Otherwise, set `pipeline_failed` to False.

7. Return value
   7.1 Return a dictionary with exactly the following keys:

       {
         "total_duration": int,
         "successful_jobs": list[str],
         "failed_jobs": list[str],
         "pending_jobs": list[str],
         "skipped_jobs": list[str],
         "unknown_status_jobs": list[str],
         "pipeline_failed": bool
       }

8. Constraints
   8.1 Use only the Python standard library.
   8.2 Do not mutate the original parsed JSON data.
   8.3 Favor clarity and defensive coding over cleverness.

9. Expected behavior
   9.1 `pipeline_failed` must be True for the provided JSON.
   9.2 `failed_jobs` must contain "test".
   9.3 `total_duration` must equal 1365.

'''


import json
import pprint


def analyze_pipeline(path: str ) -> dict:
    try:
        with open(path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"The config file can not be found or does not exits: {path}") from e
    except json.JSONDecodeError as e:
        raise ValueError(f"The config is invalid JSON: {path}") from e
    if isinstance(data, dict):
        jobs = data.get("jobs")
    elif isinstance(data, list):
        jobs = data
    else:
        raise TypeError(f"The config file must be a dictionary or list") from e
    if not isinstance(jobs, list):
        raise TypeError(f"'jobs must be a list. Instead got: {type(jobs).__name__}")
        
        
    total_duration = 0
    successful_jobs = []
    failed_jobs = []
    pending_jobs = []
    skipped_jobs = []
    unknown_status_jobs = []
    #pipeline_failed = len(failed_jobs) > 0

    for job in jobs:
        if not isinstance(job, dict):
            continue
        name = job.get("name", "<unknown>")
        status = job.get("status")
        duration = job.get("duration", 0)
        if isinstance(duration, int):
            total_duration += duration

        if status == 'failed':
            failed_jobs.append(name)
        elif status == 'success':
            successful_jobs.append(name)
        elif status == 'pending':
            pending_jobs.append(name)
        elif status == 'skipped':
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
         "pipeline_failed": len(failed_jobs) > 0
       }

if __name__ == "__main__":
    data = analyze_pipeline("/home/andre/DevOps-Practice/python-practice/problem2/pipeline-large.json")
    pprint.pprint(data, indent=4)




