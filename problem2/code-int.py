'''
Python DevOps Coding Challenge: CI/CD Pipeline Analyzer
Scenario

You are working on a DevOps team responsible for monitoring CI/CD pipeline health. 
Pipeline execution results are exported as a JSON file containing metadata about individual jobs, including execution time and status.

Your task is to write a Python function that analyzes this pipeline data 
and produces a concise summary that can be used for reporting or automation decisions.

 return {
        "total_duration": total_duration,
        "failed_jobs": failed_jobs,
        "pipeline_failed": len(failed_jobs) > 0
    }

'''

import json

def analyze_pipeline(path):
    with open(path, "r") as f:
        data = json.load(f)

    jobs = data["jobs"]

    total_duration = 0
    failed_jobs = []

    for job in jobs:
        total_duration += job["duration"]
        if job["status"] == "failed":
            failed_jobs.append(job["name"])

    return {
        "total_duration": total_duration,
        "failed_jobs": failed_jobs,
        "pipeline_failed": len(failed_jobs) > 0
    }


if __name__ == "__main__":
    result = analyze_pipeline("pipeline.json")
    print(result)

