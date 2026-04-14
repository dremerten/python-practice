import yaml
import json

REQUIRED_TOP_LEVEL_KEYS = {"pipeline_name", "environment", "stages", "jobs"}

REQUIRED_STAGE_ORDER = ["lint", "test", "build", "deploy"]

ALLOWED_RUNNER_IMAGES = {
    "python:3.11",
    "python:3.12",
    "alpine:3.20",
    "ubuntu:24.04"
  }



def validate_pipeline_structure(pipeline) -> list[str]:
    problems = []

    if not isinstance(pipeline, dict):
        return ["Invalid pipeline: not a dictionary"]
    
    missing_keys = REQUIRED_TOP_LEVEL_KEYS - pipeline.keys()
    if missing_keys:
        problems.append(f"Pipeline is missing required top-level keys: {missing_keys}")
        return problems
    
    pipeline_name = pipeline.get("pipeline_name")
    if not isinstance(pipeline_name, str) or pipeline_name.strip() == "":
        problems.append(f"Pipeline name must be a non-empty string")
    
    environment = pipeline.get("environment")
    if not isinstance(environment, str) or environment.strip() == "":
        problems.append(
            f"Environment value must be a str, got {type(environment).__name__}"
            )

    stages = pipeline.get("stages")
    if not isinstance(stages, list):
        problems.append(
            f"Stages must be defined as a list, got {type(stages).__name__}"
            )
    else:
        missing_stages = [stage for stage in REQUIRED_STAGE_ORDER if stage not in stages]
        if missing_stages:
            problems.append(f"Pipeline is missing required stages: {missing_stages}")
        if stages != REQUIRED_STAGE_ORDER:
            problems.append("Pipeline stages are not in the required order")

    jobs = pipeline.get("jobs")
    if not isinstance(jobs, dict):
        problems.append(f"Jobs must be defined as a dictionary")
    else:
        if len(jobs) <= 0:
            problems.append(f"Pipeline must define at least one job")
    
    return problems



def validate_job(job_name: str, job_data: dict, all_jobs: dict) -> list[str]:
    problems = []

    if not isinstance(job_data, dict):
        return [f"Job Data is not a dictionary"]
    
    required_keys = {"stage", "image", "script"}
    missing_keys = required_keys - job_data.keys()
    if missing_keys:
        problems.append(f"{job_name} is missing required keys: {sorted(missing_keys)}")
        return problems
    
    stage = job_data.get("stage")
    if stage not in REQUIRED_STAGE_ORDER:
        problems.append(f"{job_name} has invalid stage: {stage}")
    
    image = job_data.get("image")
    if not isinstance(image, str) or image not in ALLOWED_RUNNER_IMAGES:
        problems.append(f"{job_name} uses disallowed image: {image}")

    script = job_data.get("script")
    if not isinstance(script, list) or len(script) <= 0:
        problems.append(f"{job_name} script must be a non-empty list")
    
    env = job_data.get("env", {})
    if not isinstance(env, dict):
        problems.append(f"{job_name} env must be a dictionary")
    else:
        sensitive_keywords = {"password", "secret", "token"}
        for key, value in env.items():
            if not isinstance(value, str):
                continue
            value_lower = value.lower()
            if any(i in value_lower for i in sensitive_keywords) or value.startswith("AKIA"):
                problems.append(f"{job_name} contains hardcoded secret in env: {key}")
   
    if job_data.get("stage") == "deploy":
        branch = job_data.get("branch")
        if branch != "main":
            problems.append(f"{job_name} must deploy from main branch")

        needs = job_data.get("needs")
        if not isinstance(needs, list):
            problems.append(f"{job_name} must define dependencies as a list")
        else:
            valid = any(
                item in all_jobs and all_jobs[item].get(stage) == "test"
                for item in needs
            )
            if not valid:
                problems.append(f"{job_name} must depend on at least one test job")
    
    retries = job_data.get("retries")
    if retries is not None:
        if not isinstance(retries, int) or retries < 0 or retries > 3:
            problems.append(f"{job_name} retries must be between 0 and 3")
    
    return problems
    



def evaluate_pipeline_compliance(pipeline: dict) -> dict:
    results = {
        "compliant": False,
        "pipeline_name": None,
        "environment": None,
        "total_jobs": 0,
        "valid_jobs_count": 0,
        "failed_jobs_count": 0,
        "failed_jobs": [],
        "reasons": [],
    }

    if not isinstance(pipeline, dict):
        results["reasons"].append(f"Pipeline must be a dictionary")
        return results

    problems = validate_pipeline_structure(pipeline)
    if problems:
        results["reasons"].extend(problems)
        return results

    results["pipeline_name"] = pipeline["pipeline_name"]
    results["environment"] = pipeline["environment"]

    jobs = pipeline.get("jobs", {})
    results["total_jobs"] = len(jobs)

    for job_name, job_data in jobs.items():
        problems = validate_job(job_name, job_data, jobs)
        if problems:
            results["failed_jobs_count"] += 1
            results["failed_jobs"].append(job_name)
            results["reasons"].extend(problems)
        else:
            results["valid_jobs_count"] += 1

    if len(jobs) < 3:
        results["reasons"].append("Pipeline must define at least 3 jobs")
    if results["environment"] != "production":
        results["reasons"].append("Pipeline environment must be production")
    
    # if results["reasons"] and results["failed_jobs_count"] == 0:
    #     results["compliant"] = True
    results["compliant"] = (
        len(results["reasons"]) == 0
        and results["failed_jobs_count"] == 0
    )

    return results


if __name__ == "__main__":
    PATH = "pipeline.custom.yaml"

    try:
        with open(PATH, "r") as f:
            pipeline = yaml.safe_load(f)
        result = evaluate_pipeline_compliance(pipeline)
        print(json.dumps(result, indent=4))

    except FileNotFoundError:
        print("Pipeline file not found")

    except yaml.YAMLError:
        print("Invalid YAML format")

    ##### DEBUG #####
    # for job_name, job_data in pipeline.get("jobs", {}).items():
    #     validate_job(job_name, job_data, pipeline.get("jobs", {}))