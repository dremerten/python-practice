"""
KUBERNETES YAML AUDIT — MID-LEVEL CHECKLIST

GOAL:
Implement a function that reads a Kubernetes YAML file containing one or more
documents and produces deployment-focused audit metrics.

You are reviewing manifests to identify:
- how many resources exist per kind
- which Deployments are missing resource limits
- which Services are publicly exposed
- which containers are using the :latest tag
- which Deployments have replica counts below production expectations

YAML file may contain multiple documents separated by:
---

Each document is expected to represent one Kubernetes resource.

========================================================
1) FUNCTION SETUP
--------------------------------------------------------
[ ] Define: audit_k8s_manifests(file_path: str) -> dict

[ ] Initialize:
    - results (dict) for FINAL output:
        kind_counts -> dict[str, int]
        missing_resource_limits -> list[str]
        public_services -> list[str]
        latest_tag_images -> dict[str, list[str]]
        low_replica_deployments -> dict[str, int]

    - latest_tracker -> dict[str, list[str]]

========================================================
2) FILE HANDLING
--------------------------------------------------------
[ ] Use a try block

[ ] Open the file using a context manager

[ ] Load all YAML documents into a list

[ ] Handle:
    - file not found
    - invalid YAML

[ ] On exception:
    - print an error message
    - return results

========================================================
3) DOCUMENT LOOP
--------------------------------------------------------
[ ] Iterate through loaded documents

[ ] For each document:
    - skip empty values
    - skip non-dictionary values

========================================================
4) COMMON FIELD EXTRACTION
--------------------------------------------------------
[ ] Extract Required Fields:
    - kind
    - metadata with a safe default - {}
    - spec with a safe default - {}
    - name from metadata

[ ] If required fields are missing:
    continue

========================================================
5) KIND COUNTING
--------------------------------------------------------
[ ] Update the count for the current kind using a default value pattern:

    - Use the existing count if present
    - Otherwise default to 0
    - Then increment by 1

========================================================
6) DEPLOYMENT HANDLING
--------------------------------------------------------
[ ] Only process documents where:
    kind == "Deployment"

[ ] Extract:
    - deployment_name
    - replicas from spec using a default value of 1 if not present

========================================================
7) LOW REPLICA TRACKING
--------------------------------------------------------
[ ] If replicas < 2:
    - store deployment_name and replicas in
      results["low_replica_deployments"]

========================================================
8) CONTAINER EXTRACTION
--------------------------------------------------------
[ ] Extract:
    - template from spec using a default empty dictionary
    - template_spec from template using a default empty dictionary
    - containers from template_spec using a default empty list

[ ] If containers is not a list:
    continue

========================================================
9) MISSING RESOURCE LIMITS
--------------------------------------------------------
[ ] Initialize:
    deployment_missing_limits = False

[ ] Loop through containers

[ ] If container is not a dictionary:
    continue

[ ] Extract:
    image using default ""
    resources using default {}
    limits from resources

[ ] If limits is missing or empty:
    deployment_missing_limits = True

========================================================
10) LATEST TAG TRACKING
--------------------------------------------------------
[ ] If image is not empty:

[ ] If image ends with ":latest" or ":" is not in image:

[ ] If deployment_name is not in latest_tracker:
    latest_tracker[deployment_name] = []

[ ] If image is not already in latest_tracker[deployment_name]:
    append image

========================================================
11) FINALIZE DEPLOYMENT RESULTS
--------------------------------------------------------
[ ] If deployment_missing_limits is True:

[ ] If deployment_name is not in results["missing_resource_limits"]:
    append deployment_name

========================================================
12) SERVICE HANDLING
--------------------------------------------------------
[ ] Replace the standalone Deployment condition with:

    if kind == "Deployment":
        ...

    elif kind == "Service":

[ ] service_name = name
[ ] service_type = spec.get("type", "ClusterIP")

[ ] If service_type in ["LoadBalancer", "NodePort"]:
    results["public_services"].append(service_name)

========================================================
13) FINAL PROCESSING
--------------------------------------------------------
[ ] Sort:
    - results["missing_resource_limits"]
    - results["public_services"]

[ ] Loop through latest_tracker.items()

[ ] For each deployment_name and images:
    - store sorted(images) in
      results["latest_tag_images"][deployment_name]

========================================================
14) RETURN VALUE
--------------------------------------------------------
[ ] Return results

========================================================
15) SCRIPT ENTRY POINT
--------------------------------------------------------
[ ] Add a main guard

[ ] Inside it:
    - define the sample file path
    - call the function
    - print the returned results

========================================================
Expected Result
--------------------------------------------------------
{
    "kind_counts": {
        "Deployment": 4,
        "Service": 3,
        "ConfigMap": 2,
        "Secret": 1
    },
    "missing_resource_limits": [
        "billing-service",
        "worker-api"
    ],
    "public_services": [
        "billing-svc",
        "frontend-svc"
    ],
    "latest_tag_images": {
        "web-app": [
            "nginx:latest"
        ],
        "worker-api": [
            "mycorp/worker"
        ],
        "billing-service": [
            "python:latest"
        ]
    },
    "low_replica_deployments": {
        "worker-api": 1,
        "billing-service": 1
    }
}
"""