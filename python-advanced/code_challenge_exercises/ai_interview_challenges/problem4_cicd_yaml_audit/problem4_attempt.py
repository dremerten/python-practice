"""
DEVOPS PYTHON CHALLENGE — CI/CD PIPELINE YAML AUDIT

GOAL
------------------------------------------------
This script loads a CI/CD pipeline definition from a YAML file and evaluates
whether it meets baseline delivery, security, and deployment policy requirements.

The pipeline must define valid top-level structure and every job must pass
validation.

Pipeline-level requirements:
- Required top-level keys must exist:
  - "pipeline_name"
  - "environment"
  - "stages"
  - "jobs"
- Stages must exactly match this order:
  - lint
  - test
  - build
  - deploy
- The pipeline environment must be "production"
- The pipeline must define at least 3 jobs

Per-job requirements:
- Every job must define:
  - "stage"
  - "image"
  - "script"
- Job stage must be valid
- Job image must be in the allowed runner image list
- Job script must be a non-empty list
- Job environment variables must not contain hardcoded secret-like values
- Deploy jobs must:
  - deploy only from branch "main"
  - depend on at least one job whose stage is "test"
- If a job defines "retries", it must be an integer between 0 and 3

Pipeline compliance is ONLY true if ALL of the above conditions are satisfied.

------------------------------------------------
EXPECTED OUTPUT (HIGH LEVEL)
------------------------------------------------
The script should return a dictionary with the following structure:

{
    "compliant": bool,
    "pipeline_name": str | None,
    "environment": str | None,
    "total_jobs": int,
    "valid_jobs_count": int,
    "failed_jobs_count": int,
    "failed_jobs": list[str],
    "reasons": list[str],
}
"""

import pprint
import yaml

REQUIRED_TOP_LEVEL_KEYS = {
    "pipeline_name",
    "environment",
    "stages",
    "jobs",
}

REQUIRED_STAGE_ORDER = [
    "lint",
    "test",
    "build",
    "deploy",
]

ALLOWED_RUNNER_IMAGES = {
    "python:3.11",
    "python:3.12",
    "alpine:3.20",
    "ubuntu:24.04",
}


def validate_pipeline_structure(pipeline: dict) -> list[str]:
    # TODO: create list to store validation errors
    # - problems = []
    problems = []

    # TODO: if pipeline is not a dictionary:
    # - return ["Invalid pipeline: not a dictionary"]
    if not isinstance(pipeline, dict):
        return ["Invalid pipeline: not a dictionary"]

    # TODO: compute missing top-level keys:
    # - missing_keys = REQUIRED_TOP_LEVEL_KEYS - pipeline.keys()
    # - if missing_keys is not empty:
    #     - append to problems:
    #       f"Pipeline is missing required top-level keys: {sorted(missing_keys)}"
    #     - return problems
    missing_keys = REQUIRED_TOP_LEVEL_KEYS - pipeline.keys()
    if missing_keys:
        problems.append(f"Pipeline is missing required top-level keys: {sorted(missing_keys)}")
        return problems
    
    # TODO: validate pipeline_name:
    # - pipeline_name = pipeline.get("pipeline_name")
    # - if NOT isinstance(pipeline_name, str) OR pipeline_name.strip() == "":
    #     - append to problems:
    #       "Pipeline name must be a non-empty string"
    pipeline_name = pipeline.get("pipeline_name")
    if not isinstance(pipeline_name, str) or pipeline_name.strip() == "":
        problems.append(f"Pipeline name must be a non-empty string")

    # TODO: validate environment:
    # - environment = pipeline.get("environment")
    # - if NOT isinstance(environment, str) OR environment.strip() == "":
    #     - append to problems:
    #       "Pipeline environment must be a non-empty string"
    environment = pipeline.get("environment")
    if not isinstance(environment, str) or environment.strip() == "":
        problems.append(f"Pipeline environment must be a non-empty string")

    # TODO: validate stages:
    # - stages = pipeline.get("stages")
    # - if NOT isinstance(stages, list):
    #     - append to problems:
    #       "Stages must be defined as a list"
    # - else:
    #     - missing_stages = [s for s in REQUIRED_STAGE_ORDER if s not in stages]
    #     - if missing_stages is not empty:
    #         - append to problems:
    #           f"Pipeline is missing required stages: {missing_stages}"
    #     - if stages != REQUIRED_STAGE_ORDER:
    #         - append to problems:
    #           "Pipeline stages are not in the required order"
    stages = pipeline.get("stages")
    if not isinstance(stages, list):
        problems.append(f"Stages must be defined as a list")
    else:
        missing_stages = [s for s in REQUIRED_STAGE_ORDER if s not in stages]
        if missing_stages:
            problems.append(f"Pipeline is missing required stages: {missing_stages}")
        if stages != REQUIRED_STAGE_ORDER:
            problems.append(f"Pipeline stages are not in the required order")

    # TODO: validate jobs:
    # - jobs = pipeline.get("jobs")
    # - if NOT isinstance(jobs, dict):
    #     - append to problems:
    #       "Jobs must be defined as a dictionary"
    # - elif len(jobs) == 0:
    #     - append to problems:
    #       "Pipeline must define at least one job"
    jobs = pipeline.get("jobs")
    if not isinstance(jobs, dict):
        problems.append(f"Jobs must be defined as a dictionary")
    elif len(jobs) == 0:
        problems.append(f"Pipeline must define at least one job")

    # TODO: return problems
    return problems


def validate_job(job_name: str, job_data: dict, all_jobs: dict) -> list[str]:
    # TODO: create list to store job validation errors
    # - problems = []
    problems = []

    # TODO: if job_data is not a dictionary:
    # - return [f"{job_name} is invalid: job definition is not a dictionary"]
    if not isinstance(job_data, dict):
        return [f"{job_name} is invalid: job definition is not a dictionary"]

    # TODO: validate required fields:
    # - required_keys = {"stage", "image", "script"}
    # - missing_keys = required_keys - job_data.keys()
    # - if missing_keys is not empty:
    #     - append to problems:
    #       f"{job_name} is missing required keys: {sorted(missing_keys)}"
    #     - return problems
    required_keys = {"stage", "image", "script"}
    missing_keys = required_keys - job_data.keys()
    if missing_keys:
        problems.append(f"{job_name} is missing required keys: {sorted(missing_keys)}")
        return problems

    # TODO: validate stage:
    # - stage = job_data.get("stage")
    # - if stage NOT IN REQUIRED_STAGE_ORDER:
    #     - append to problems:
    #       f"{job_name} has invalid stage: {stage}"
    stage = job_data.get("stage")
    if stage not in REQUIRED_STAGE_ORDER:
        problems.append(f"{job_name} has invalid stage: {stage}")

    # TODO: validate image:
    # - image = job_data.get("image")
    # - if NOT isinstance(image, str) OR image NOT IN ALLOWED_RUNNER_IMAGES:
    #     - append to problems:
    #       f"{job_name} uses disallowed image: {image}"
    image = job_data.get("image")
    if not isinstance(image, str) or image not in ALLOWED_RUNNER_IMAGES:
        problems.append(f"{job_name} uses disallowed image: {image}")

    # TODO: validate script:
    # - script = job_data.get("script")
    # - if NOT isinstance(script, list) OR len(script) == 0:
    #     - append to problems:
    #       f"{job_name} script must be a non-empty list"
    script = job_data.get("script")
    if not isinstance(script, list) or len(script) == 0:
        problems.append(f"{job_name} script must be a non-empty list")

    # TODO: validate env:
    # - env = job_data.get("env", {})
    # - if NOT isinstance(env, dict):
    #     - append to problems:
    #       f"{job_name} env must be a dictionary"
    # - else:
    #     - for key, value in env.items():
    #         - if isinstance(value, str) AND (
    #               "password" in value.lower()
    #               OR "secret" in value.lower()
    #               OR "token" in value.lower()
    #               OR value.startswith("AKIA")
    #           ):
    #             - append to problems:
    #               f"{job_name} contains hardcoded secret in env: {key}"
    env = job_data.get("env", {})
    if not isinstance(env, dict):
        problems.append(f"{job_name} env must be a dictionary")
    else:
        for key, value in env.items():
            if isinstance(value, str) and (
                "password" in value.lower()
                or "secret" in value.lower()
                or "token" in value.lower()
                or value.startswith("AKIA")
            ):
                problems.append(f"{job_name} contains hardcoded secret in env: {key}")

    # TODO: validate deploy branch:
    # - if job_data.get("stage") == "deploy":
    #     - branch = job_data.get("branch")
    #     - if branch != "main":
    #         - append to problems:
    #           f"{job_name} must deploy from main branch"
    if job_data.get("stage") == "deploy":
        branch = job_data.get("branch")
        if branch != "main":
            problems.append(f"{job_name} must deploy from main branch")

    # TODO: validate deploy dependencies:
    # - if job_data.get("stage") == "deploy":
    #     - needs = job_data.get("needs")
    #     - if NOT isinstance(needs, list):
    #         - append to problems:
    #           f"{job_name} must define dependencies as a list"
    #     - else:
    #         - valid = any(
    #               dep in all_jobs AND all_jobs[dep].get("stage") == "test"
    #           for dep in needs)
    #         - if NOT valid:
    #             - append to problems:
    #               f"{job_name} must depend on at least one test job"
    if job_data.get("stage") == "deploy":
        needs = job_data.get("needs")
        if not isinstance(needs, list):
            problems.append(f"{job_name} must define dependencies as a list")
        else:
            valid = any(
                dep in all_jobs and all_jobs[dep].get("stage") == "test"
                for dep in needs)
            if not valid:
                problems.append(f"{job_name} must depend on at least one test job")

    # TODO: validate retries:
    # - retries = job_data.get("retries")
    # - if retries is not None:
    #     - if NOT isinstance(retries, int) OR retries < 0 OR retries > 3:
    #         - append to problems:
    #           f"{job_name} retries must be between 0 and 3"
    retries = job_data.get("retries")
    if retries is not None:
        if not isinstance(retries, int) or retries < 0 or retries > 3:
            problems.append(f"{job_name} retries must be between 0 and 3")

    # TODO: return problems
    return problems


def evaluate_pipeline_compliance(pipeline: dict) -> dict:
    # TODO: initialize result dictionary
    result = {
    "compliant": False,
    "pipeline_name": None,
    "environment": None,
    "total_jobs": 0,
    "valid_jobs_count": 0,
    "failed_jobs_count": 0,
    "failed_jobs": [],
    "reasons": [],
    }

    # TODO: validate structure:
    # - problems = validate_pipeline_structure(pipeline)
    # - if problems:
    #     - extend result["reasons"] with problmes
    #     - return result
    problems = validate_pipeline_structure(pipeline)
    if problems:
        result["reasons"].extend(problems)
        return result

    # TODO: extract metadata:
    # - result["pipeline_name"] = pipeline.get("pipeline_name")
    # - result["environment"] = pipeline.get("environment")
    result["pipeline_name"] = pipeline.get("pipeline_name")
    result["environment"] = pipeline.get("environment")

    # TODO: extract jobs:
    # - jobs = pipeline.get("jobs", {})
    # - result["total_jobs"] = len(jobs)
    jobs = pipeline.get("jobs", {})
    result["total_jobs"] = len(jobs)

    # TODO: iterate jobs:
    # - for job_name, job_data in jobs.items():
    #     - problems = validate_job(job_name, job_data, jobs)
    #     - if problems:
    #         - result["failed_jobs_count"] += 1
    #         - result["failed_jobs"].append(job_name)
    #         - result["reasons"].extend(problems)
    #     - else:
    #         - result["valid_jobs_count"] += 1
    for job_name, job_data in jobs.items():
        problems = validate_job(job_name, job_data, jobs)
        if problems:
            result["failed_jobs_count"] += 1
            result["failed_jobs"].append(job_name)
            result["reasons"].extend(problems)
        else:
            result["valid_jobs_count"] += 1

    # TODO: enforce minimum jobs:
    # - if len(jobs) < 3:
    #     - result["reasons"].append("Pipeline must define at least 3 jobs")
    if len(jobs) < 3:
        result["reasons"].append(f"Pipeline must define at least 3 jobs")

    # TODO: enforce production:
    # - if result["environment"] != "production":
    #     - result["reasons"].append("Pipeline environment must be production")
    if result["environment"] != "production":
        result["reasons"].append("Pipeline environment must be production")

    # TODO: final decision:
    # - result["compliant"] = (
    #     len(result["reasons"]) == 0
    #     and result["failed_jobs_count"] == 0
    # )
    result["compliant"] = (
        len(result["reasons"]) == 0
        and result["failed_jobs_count"] == 0
    )

    # TODO: return result
    return result


if __name__ == "__main__":
    PATH = "pipeline.custom.yaml"

    try:
        with open(PATH, "r") as f:
            pipeline = yaml.safe_load(f)
        result = evaluate_pipeline_compliance(pipeline)
        pprint.pprint(result)

    except FileNotFoundError:
        print("Pipeline file not found")

    except yaml.YAMLError:
        print("Invalid YAML format")