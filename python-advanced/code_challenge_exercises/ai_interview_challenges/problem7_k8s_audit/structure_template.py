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

# 1. Import modules (json, yaml)
# 2. Define function with type hints - def audit_k8s_manifests(file_path: str) -> dict:
# 3. Initialize results dict
 results = {
        "kind_counts": {},
        "missing_resource_limits": [],
        "public_services": [],
        "latest_tag_images": {},
        "low_replica_deployments": {}
    }

# 4. Initialize latest_tracker dict (stores images per deployment name before final sorting)

# 5. Open YAML file in try/except block
    # 6. Catch FileNotFoundError with descriptive message
    # 7. Catch invalid YAML exception — print error, return results
    # 8. Load all YAML documents into a list (file may contain multiple documents separated by ---)

    # 9. Loop through loaded documents
        # 10. Skip document if it is empty or not a dictionary

        # 11. Extract kind, metadata (default {}), spec (default {}), name from metadata
        # 12. Skip document if kind or name are missing

        # 13. Update kind_counts[kind] running total (use .get(kind, 0) + 1)

        # 14. If kind == "Deployment":
            # 15. Set deployment_name = name and extract replicas from spec (default 1 if not present)

            # 16. If replicas < 2, store deployment_name and replicas in results["low_replica_deployments"]

            # 17. Extract template from spec (default {}), 
                  - template_spec from template (default {}), 
                  - containers from template_spec (default [])
            # 18. If containers is not a list, skip this document

            # 19. Initialize deployment_missing_limits = False

            # 20. Loop through containers
                # 21. Skip container if it is not a dictionary
                # 22. Extract image (default ""), 
                      - resources (default {}), 
                      - limits from resources

                # 23. If limits is missing or empty, set deployment_missing_limits = True

                # 24. If image is non-empty AND (image ends with ":latest" OR ":" is not in image):
                    # 25. Initialize latest_tracker[deployment_name] to empty list if not yet a key
                    # 26. Append image to latest_tracker[deployment_name] list if not already in it

            # 27. If deployment_missing_limits is True and deployment_name not already in results["missing_resource_limits"], append deployment_name

        # 28. elif kind == "Service":
            # 29. Set service_name = name and extract service_type from spec (default "ClusterIP")
            # 30. If service_type is "LoadBalancer" or "NodePort", append service_name to results["public_services"]

# 31. Post-loop: sort results["missing_resource_limits"] in place
# 32. Post-loop: sort results["public_services"] in place
# 33. Post-loop: iterate latest_tracker.items() — 
#       for each (deployment_name, images), store sorted(images) 
#       in results["latest_tag_images"][deployment_name]

# 34. Return results

# 35. Add main guard — define sample file path, call function, print results

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


"""
single doc referrence

{
    "apiVersion": "apps/v1",
    "kind": "Deployment",
    "metadata": {
        "name": "web-app",
        "namespace": "production",
        "labels": {
            "app": "web-app",
            "tier": "frontend",
            "team": "platform",
            "env": "prod"
        }
    },
    "spec": {
        "replicas": 3,
        "revisionHistoryLimit": 5,
        "selector": {
            "matchLabels": {
                "app": "web-app"
            }
        },
        "strategy": {
            "type": "RollingUpdate",
            "rollingUpdate": {
                "maxUnavailable": 1,
                "maxSurge": 1
            }
        },
        "template": {
            "metadata": {
                "labels": {
                    "app": "web-app",
                    "tier": "frontend",
                    "env": "prod"
                },
                "annotations": {
                    "prometheus.io/scrape": "true",
                    "prometheus.io/port": "9113"
                }
            },
            "spec": {
                "serviceAccountName": "web-app-sa",
                "securityContext": {
                    "fsGroup": 2000
                },
                "containers": [
                    {
                        "name": "nginx",
                        "image": "nginx:latest",
                        "imagePullPolicy": "Always",
                        "ports": [
                            {
                                "name": "http",
                                "containerPort": 80
                            },
                            {
                                "name": "metrics",
                                "containerPort": 9113
                            }
                        ],
                        "env": [
                            {
                                "name": "NGINX_PORT",
                                "value": "80"
                            },
                            {
                                "name": "APP_ENV",
                                "value": "production"
                            },
                            {
                                "name": "CACHE_ENABLED",
                                "value": "true"
                            }
                        ],
                        "envFrom": [
                            {
                                "configMapRef": {
                                    "name": "web-app-config"
                                }
                            }
                        ],
                        "volumeMounts": [
                            {
                                "name": "nginx-cache",
                                "mountPath": "/var/cache/nginx"
                            },
                            {
                                "name": "nginx-tmp",
                                "mountPath": "/tmp"
                            }
                        ],
                        "readinessProbe": {
                            "httpGet": {
                                "path": "/healthz",
                                "port": "http"
                            },
                            "initialDelaySeconds": 5,
                            "periodSeconds": 10,
                            "timeoutSeconds": 2,
                            "failureThreshold": 3
                        },
                        "livenessProbe": {
                            "httpGet": {
                                "path": "/livez",
                                "port": "http"
                            },
                            "initialDelaySeconds": 15,
                            "periodSeconds": 20,
                            "timeoutSeconds": 2,
                            "failureThreshold": 3
                        },
                        "startupProbe": {
                            "httpGet": {
                                "path": "/startupz",
                                "port": "http"
                            },
                            "failureThreshold": 30,
                            "periodSeconds": 5
                        },
                        "resources": {
                            "requests": {
                                "cpu": "150m",
                                "memory": "192Mi"
                            },
                            "limits": {
                                "cpu": "500m",
                                "memory": "512Mi"
                            }
                        },
                        "securityContext": {
                            "allowPrivilegeEscalation": false,
                            "readOnlyRootFilesystem": true
                        }
                    }
                ],
                "volumes": [
                    {
                        "name": "nginx-cache",
                        "emptyDir": {}
                    },
                    {
                        "name": "nginx-tmp",
                        "emptyDir": {}
                    }
                ]
            }
        }
    }
}
"""