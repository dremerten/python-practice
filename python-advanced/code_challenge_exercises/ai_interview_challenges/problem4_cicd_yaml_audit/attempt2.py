import pprint
import yaml

REQUIRED_TOP_LEVEL_KEYS = {"pipeline_name", "environment", "stages", "jobs"}
REQUIRED_STAGE_ORDER = ["lint", "test", "build", "deploy"]
ALLOWED_RUNNER_IMAGES = {
    "python:3.11",
    "python:3.12",
    "alpine:3.20",
    "ubuntu:24.04",
}


def validate_pipeline_structure(pipeline: dict) -> list[str]:
    problems = []

    if not isinstance(pipeline, dict):
        return ["Invalid pipeline: not a dictionary"]

    missing_keys = [key for key in REQUIRED_TOP_LEVEL_KEYS if key not in pipeline]
    if missing_keys:
        problems.append(f"Pipeline is missing required top-level keys: {missing_keys}")
        return problems

    pipeline_name = pipeline.get("pipeline_name")
    if not isinstance(pipeline_name, str) or pipeline_name.strip() == "":
        problems.append("Pipeline name must be a non-empty string")

    environment = pipeline.get("environment")
    if not isinstance(environment, str) or environment.strip() == "":
        problems.append("Pipeline environment must be a non-empty string")

    stages = pipeline.get("stages", [])
    if not isinstance(stages, list):
        problems.append("Stages must be defined as a list")
    else:
        missing_stages = [
            stage_name
            for stage_name in REQUIRED_STAGE_ORDER
            if stage_name not in stages
        ]
        if missing_stages:
            problems.append(f"Pipeline is missing required stages: {missing_stages}")

        if stages != REQUIRED_STAGE_ORDER:
            problems.append("Pipeline stages are not in the required order")

    jobs = pipeline.get("jobs")
    if not isinstance(jobs, dict):
        problems.append("Jobs must be defined as a dictionary")
    elif len(jobs) == 0:
        problems.append("Pipeline must define at least one job")

    return problems


def validate_job(job_name, job_data, all_jobs):
    problems = []

    if not isinstance(job_data, dict):
        return [f"{job_name} must be defined as a dictionary"]

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
    if not isinstance(script, list) or len(script) == 0:
        problems.append(f"{job_name} script must be a non-empty list")
        return problems

    env = job_data.get("env", {})
    if not isinstance(env, dict):
        problems.append(f"{job_name} env must be a dictionary")
    else:
        sensitive_keywords = {"password", "secret", "token"}

        for key, value in env.items():
            key_lower = str(key).lower()
            value_lower = value.lower() if isinstance(value, str) else ""

            if (
                any(keyword in key_lower for keyword in sensitive_keywords)
                or any(keyword in value_lower for keyword in sensitive_keywords)
                or (isinstance(value, str) and value.startswith("AKIA"))
            ):
                problems.append(f"{job_name} contains hardcoded secret in env: {key}")

    if stage == "deploy":
        branch = job_data.get("branch")
        if branch != "main":
            problems.append(f"{job_name} must deploy from main branch")

    if stage == "deploy":
        needs = job_data.get("needs")
        if not isinstance(needs, list):
            problems.append(f"{job_name} must define dependencies as a list")
        else:
            valid = any(
                dep in all_jobs and all_jobs[dep].get("stage") == "test"
                for dep in needs
            )
            if not valid:
                problems.append(f"{job_name} must depend on at least one test job")

    retries = job_data.get("retries")
    if retries is not None:
        if not isinstance(retries, int) or retries < 0 or retries > 3:
            problems.append(f"{job_name} retries must be between 0 and 3")

    return problems


def evaluate_pipeline_compliance(pipeline: dict) -> dict:
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

    problems = validate_pipeline_structure(pipeline)
    if problems:
        result["reasons"].extend(problems)
        return result

    result["pipeline_name"] = pipeline.get("pipeline_name")
    result["environment"] = pipeline.get("environment")

    jobs = pipeline.get("jobs", {})
    result["total_jobs"] = len(jobs)

    for job_name, job_data in jobs.items():
        problems = validate_job(job_name, job_data, jobs)
        if problems:
            result["failed_jobs_count"] += 1
            result["failed_jobs"].append(job_name)
            result["reasons"].extend(problems)
        else:
            result["valid_jobs_count"] += 1

    if len(jobs) < 3:
        result["reasons"].append("Pipeline must define at least 3 jobs")

    if result["environment"] != "production":
        result["reasons"].append("Pipeline environment must be production")

    if len(result["reasons"]) == 0 and result["failed_jobs_count"] == 0:
        result["compliant"] = True

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