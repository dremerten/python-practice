"""
CI/CD PIPELINE AUDIT — INTERVIEW PSEUDOCODE

----------------------------------------
EXPECTED FUNCTION NAMES (DO NOT CHANGE)
----------------------------------------

validate_pipeline_structure(pipeline)
→ returns: LIST of STRING errors

validate_job(job_name, job_data, all_jobs)
→ returns: LIST of STRING errors

evaluate_pipeline_compliance(pipeline)
→ returns: DICTIONARY (final result)

----------------------------------------
CONSTANTS (DEFINE THESE EXACTLY)
----------------------------------------
import pprint
import yaml


REQUIRED_TOP_LEVEL_KEYS
→ SET of STRINGS
→ {"pipeline_name", "environment", "stages", "jobs"}

REQUIRED_STAGE_ORDER
→ LIST of STRINGS (ORDER MATTERS)
→ ["lint", "test", "build", "deploy"]

ALLOWED_RUNNER_IMAGES
→ SET of STRINGS
→ {
    "python:3.11",
    "python:3.12",
    "alpine:3.20",
    "ubuntu:24.04"
  }

----------------------------------------
STRUCTURE VALIDATION
----------------------------------------

validate_pipeline_structure(pipeline):

- Create an empty LIST called "problems"
  → this will collect all validation errors

- If pipeline is not DICTIONARY:
  → return ["Invalid pipeline: not a dictionary"]

VALIDATE REQUIRED TOP-LEVEL KEYS

- Create a list named missing_keys

- For each key in REQUIRED_TOP_LEVEL_KEYS:
    if that key is not present in pipeline:
        append that key to missing_keys

- If missing_keys is not empty:
    append
    "Pipeline is missing required top-level keys: [missing_keys]"
    to problems

    return problems immediately

VALIDATE pipeline_name

- Read the value for key "pipeline_name" using a safe lookup

- Evaluate this condition:

    value is not a string
    OR
    value, after removing leading/trailing whitespace, is empty

- If the condition is true:
    append "Pipeline name must be a non-empty string" to problems

# Validate environment:
#   → must be STRING OR after stripping whitespace, must not be empty
#   → if invalid → append error to problems

VALIDATE STAGES

- Read the value stored at key "stages" from pipeline

- If that value is not a list:
  → append "Stages must be defined as a list" to problems

- Else:

  - Create a list named missing_stages

  - For each stage name in REQUIRED_STAGE_ORDER:
      if that stage name is not present in stages:
        append that stage name to missing_stages

  - If missing_stages is not empty:
      append
      "Pipeline is missing required stages: [missing_stages]"
      to problems

  - If stages is not exactly equal to REQUIRED_STAGE_ORDER:
      append
      "Pipeline stages are not in the required order"
      to problems

VALIDATE JOBS

- Read the value stored at key "jobs" from pipeline

- If that value is not a dictionary:
  → append "Jobs must be defined as a dictionary" to problems

- Else if the number of items in jobs is 0:
  → append "Pipeline must define at least one job" to problems

- Return problems
  → an empty problems list means the jobs section is valid

----------------------------------------
JOB VALIDATION
----------------------------------------

validate_job(job_name, job_data, all_jobs):

- Create an empty LIST called "problems"

- If job_data is not DICTIONARY:
  → return [error]

# Required keys:
#   → define a set called required_keys as: "stage", "image", "script"
#   → compute missing keys as the difference between required_keys and job_data keys
#   → if missing keys is not empty → append "{job_name} is missing required keys: [sorted missing keys]" to problems
#   → return problems

- Validate stage:
  → get the value of "stage"
  → if stage is not in REQUIRED_STAGE_ORDER
      → append "{job_name} has invalid stage: {stage}" to problems

- Validate image:
  → get the value of "image"
  → if image is not a string or not in ALLOWED_RUNNER_IMAGES
      → append f"{job_name} uses disallowed image: {image}" to problems

- Validate script:
  → get the value of "script"
  → if script is not a list or its length is 0
      → append f"{job_name} script must be a non-empty list" to problems

- Validate env:
  → get the value of "env", defaulting to an empty dictionary
  → if env is not a dictionary
      → append "{job_name} env must be a dictionary" to problems
  → otherwise
      → define a set of sensitive keywords: "password", "secret", "token"
      → for each key and value in env.items()
          → if value is not a string
              → skip to the next item
          → convert value to lowercase and assign to value_lower
          → use any() to check if any keyword in sensitive_keywords is contained 
          in the value_lower OR if value startswith() "AKIA"
          → if either condition is true
              → append f"{job_name} contains hardcoded secret in env: {key}" to problems

- Check whether the value of "stage" is "deploy"
  → If it is, continue with the deploy validations

- Validate branch
  → Get the value of "branch"
  → If branch is not equal to "main"
      → Append f"{job_name} must deploy from main branch" to problems

- Validate needs
  → Get the value of "needs"
  → If needs is not a list
      → Append f"{job_name} must define dependencies as a list" to problems
  → Otherwise
      → Define valid using any()
          → Pass a condition that loops through each item in needs
          → For each item, check:
              • it exists in all_jobs
              • and its stage in all_jobs is "test"
      → If valid is False
          → Append f"{job_name} must depend on at least one test job" to problems

- Validate retries:

  → get the value of "retries"
  → if retries is not None
      → if retries is not an integer or is less than 0 or greater than 3
          → append f"{job_name} retries must be between 0 and 3" to problems

- Return problems

----------------------------------------
EVALUATION FLOW
----------------------------------------

define evaluate_pipeline_compliance(pipeline):

- Create result DICTIONARY with initial values:
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

- Call validate_pipeline_structure and assign result to problems

  If problems is not empty:
    → extend result["reasons"] with problems
    → return result immediately

- Extract values from pipeline:
  → assign pipeline_name from pipeline["pipeline_name"] to result["pipeline_name"]
  → assign environment from pipeline["environment"] to result["environment"]
  → get jobs from pipeline (default to empty dictionary if missing)

- Set total_jobs:
  → assign the number of items in jobs to result["total_jobs"]

- For each job in jobs:
  → iterate through each job_name and job_data in jobs.items()
  → call validate_job(job_name, job_data, jobs) and assign the result to problems
  → if problems is not empty:
      → increment result["failed_jobs_count"] by 1
      → append job_name to result["failed_jobs"]
      → extend result["reasons"] with problems
  → otherwise:
      → increment result["valid_jobs_count"] by 1

- Apply global rules:
  → if the number of jobs is less than 3
      → append "Pipeline must define at least 3 jobs" to result["reasons"]
  → if result["environment"] is not equal to "production"
      → append "Pipeline environment must be production" to result["reasons"]

- Final decision:
  → if result["reasons"] is empty and result["failed_jobs_count"] equals 0
      → set result["compliant"] to True

- Return result

----------------------------------------
EXPECTED RESULT (FOR PROVIDED PIPELINE)
----------------------------------------

{
    "compliant": false,
    "pipeline_name": "sample-ci-pipeline",
    "environment": "staging",
    "total_jobs": 6,
    "valid_jobs_count": 2,
    "failed_jobs_count": 4,
    "failed_jobs": [
        "build-job",
        "deploy-job",
        "insecure-job",
        "bad-structure-job"
    ],
    "reasons": [
        "build-job uses disallowed image: python:latest",
        "deploy-job must deploy from main branch",
        "deploy-job must depend on at least one test job",
        "insecure-job contains hardcoded secret in env: PASSWORD",
        "bad-structure-job script must be a non-empty list",
        "bad-structure-job must deploy from main branch",
        "bad-structure-job must define dependencies as a list",
        "Pipeline environment must be production"
    ]
}


if __name__ == "__main__:
    - Define PATH as "pipeline.custom.yaml"

    - Try:
    → open the file at PATH in read mode
    → load YAML content using yaml.safe_load and assign to pipeline
    → call evaluate_pipeline_compliance(pipeline) and assign to result
    → print result using pprint

    - Handle exceptions:
    → if FileNotFoundError occurs
        → print "Pipeline file not found"
    → if yaml.YAMLError occurs
        → print "Invalid YAML format"
"""