import json
import yaml


def audit_k8s_manifests(file_path: str) -> dict:
    results = {
        "kind_counts": {},
        "missing_resource_limits": [],
        "public_services": [],
        "latest_tag_images": {},
        "low_replica_deployments": {}
    }

    latest_tracker = {}

    try:
        with open(file_path, 'r') as file:
            documents = list(yaml.safe_load_all(file))

            for doc in documents:
                if not isinstance(doc, dict):
                    continue

                kind = doc.get("kind")
                metadata = doc.get("metadata", {})
                spec = doc.get("spec", {})
                name = metadata.get("name")
                if not kind or not name:
                    continue

                results["kind_counts"][kind] = results["kind_counts"].get(kind, 0) + 1
                if kind == "Deployment":
                    deployment_name = name
                    replicas = spec.get("replicas", 1)

                    if replicas < 2:
                        results["low_replica_deployments"][deployment_name] = replicas

                    template = spec.get("template", {})
                    template_spec = template.get("spec", {})
                    containers = template_spec.get("containers", [])
                    if not isinstance(containers, list):
                        continue

                    deployment_missing_limits = False

                    for container in containers:
                        if not isinstance(container, dict):
                            continue

                        image = container.get("image", "")
                        resources = container.get("resources", {})
                        limits = resources.get("limits")
                        if not limits:
                            deployment_missing_limits = True

                        if image and image.endswith("latest") or ":" not in image:
                            latest_tracker.setdefault(deployment_name, []).append(image)

                        if deployment_missing_limits is True and deployment_name not in results["missing_resource_limits"]:
                            results["missing_resource_limits"].append(deployment_name)

                elif kind == "Service":
                    service_name = name
                    service_type = spec.get("type", "ClusterIP")

                    if service_type == "LoadBalancer" or service_type == "NodePort":
                        results["public_services"].append(service_name)

    except FileNotFoundError:
        print(f"The file {file_path} could not be found or does not exist.")
        return results
    except yaml.YAMLError as err:
        print(f"The file is invalid YAML: {err}")

    results["missing_resource_limits"].sort()
    results["public_services"].sort()

    for deployment_name, images in latest_tracker.items():
        results["latest_tag_images"][deployment_name] = sorted(images)

    return results

if __name__ == "__main__":
    results = audit_k8s_manifests("k8s-audit-sample.yaml")
    print(json.dumps(results, indent=4))