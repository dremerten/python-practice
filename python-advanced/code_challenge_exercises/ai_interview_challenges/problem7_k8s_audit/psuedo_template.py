"""
KUBERNETES YAML AUDIT — MID-LEVEL CHALLENGE

GOAL:
Read a Kubernetes YAML file containing one or more resource documents
and produce deployment-focused audit metrics.

You are reviewing manifests to identify:
- how many resources exist per kind
- which Deployments are missing resource limits
- which Services are publicly exposed
- which containers are using the :latest tag
- which Deployments have replica counts below production expectations

YAML files may contain multiple documents separated by "---".
Each document represents one Kubernetes resource.

========================================================
DEPENDENCIES
--------------------------------------------------------
You will need to import: json, yaml

yaml is not part of the standard library — install it with:
    pip install pyyaml

To load all documents from a multi-document YAML file use:
    yaml.safe_load_all(f)

This returns a generator. Convert it to a list so you can
iterate through it multiple times if needed.

========================================================
FUNCTION SIGNATURE
--------------------------------------------------------
audit_k8s_manifests(file_path: str) -> dict

Return shape:
    {
        kind_counts:               dict[str, int]
        missing_resource_limits:   list[str]
        public_services:           list[str]
        latest_tag_images:         dict[str, list[str]]
        low_replica_deployments:   dict[str, int]
    }

========================================================
TRACKING STATE
--------------------------------------------------------
Initialize your results dict with the return shape above.

Also initialize one helper dict outside the document loop:

    latest_tracker   dict[str, list[str]]  — collects image names per
                                             deployment before deduplication
                                             and sorting at the end

Unlike the results dict, latest_tracker holds raw intermediate
data that gets cleaned up in the post-loop step before being
written to results["latest_tag_images"].

========================================================
FILE HANDLING
--------------------------------------------------------
Wrap everything in a try/except block. Unlike the NGINX challenge
where you raised the error, here you should:
    - print a descriptive error message on FileNotFoundError
      or yaml.YAMLError
    - return the empty results dict early so the function
      exits cleanly instead of crashing

========================================================
DOCUMENT LOOP
--------------------------------------------------------
Iterate through your list of loaded documents. Each document
is one Kubernetes resource (a dict). Before doing anything
with a document:
    - skip it if it is None or empty
    - skip it if it is not a dictionary

For each valid document, extract these common fields first
since every resource type needs them:

    kind      — the resource type e.g. "Deployment", "Service"
    metadata  — safe default: {}
    spec      — safe default: {}
    name      — pull from metadata; safe default: ""

    If kind or name are missing/empty, skip the document.

Use dict.get(key, default) for all of these — YAML documents
won't always have every field present.

========================================================
KIND COUNTING
--------------------------------------------------------
Every document that passes validation gets counted regardless
of its kind. Increment the count for the current kind in
results["kind_counts"] using dict.get(key, default) so you
don't need to check if the key exists first.

========================================================
DEPLOYMENT HANDLING
--------------------------------------------------------
Use if/elif blocks to branch on kind. Start with Deployments.

    if kind == "Deployment":

        Extract from spec:
            set name and store it in deployment_name
            replicas — default to 1 if not present

        Low replica check:
            If replicas < 2, store the deployment name and
            replica count in results["low_replica_deployments"]

        Container extraction:
            Kubernetes nests containers under:
                spec -> template -> spec -> containers

            Use chained .get() calls with safe defaults ({} or [])
            at each level to avoid KeyErrors on missing fields.

            If what you get back for containers is not a list, skip
            this deployment entirely with continue.

        Per-container logic:
            Loop through containers. Skip any container that is
            not a dictionary.

            For each valid container extract:
                image      — default ""
                resources  — default {}
                limits     — pull from resources; no default needed

            Missing resource limits check:
                Initialize a flag before the container loop:
                    deployment_missing_limits = False

                If limits is missing or empty, set the flag to True.
                Don't append anything yet — wait until after the
                container loop to act on the flag.

            Latest tag check:
                If image is not empty AND the image ends with ":latest"
                OR ":" is not in the image at all (meaning no tag was
                specified, which implies latest):

                    Add the image to latest_tracker under the deployment
                    name. Initialize the list first if the deployment
                    isn't a key yet. Only append if the image isn't
                    already in the list — avoid duplicates here.

        After the container loop:
            If deployment_missing_limits is True and the deployment
            name isn't already in results["missing_resource_limits"],
            append it.

========================================================
SERVICE HANDLING
--------------------------------------------------------
    elif kind == "Service":

        Extract from spec:
            type — default "ClusterIP" if not present

        Kubernetes Services expose workloads publicly when their
        type is "LoadBalancer" or "NodePort". If the service type
        matches either of those, append the service name to
        results["public_services"].

========================================================
POST-LOOP COMPUTATION
--------------------------------------------------------
After all documents are processed:

    Sort results["missing_resource_limits"] in place
    Sort results["public_services"] in place

    Populate results["latest_tag_images"] from latest_tracker:
        Iterate latest_tracker using .items()
        For each deployment name and its image list,
        store a sorted copy of the list under the same
        key in results["latest_tag_images"]

========================================================
EXPECTED OUTPUT
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
        "web-app":          ["nginx:latest"],
        "worker-api":       ["mycorp/worker"],
        "billing-service":  ["python:latest"]
    },
    "low_replica_deployments": {
        "worker-api": 1,
        "billing-service": 1
    }
}
"""