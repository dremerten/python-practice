import yaml
import json


def analyze_cluster_manifests(manifest_file_path: str) -> dict:
    results = {
    "deployment_count": 0,
    "namespace_counts": {},
    "image_repository_counts": {},
    "largest_deployment_by_container_count": None,
    "deployments_missing_limits": [],
    "deployments_with_node_selector": {},
    "env_name_counts": {},
    "average_cpu_request_millicores": None,
    }


    # Helpers
    namespace_counts = {}
    image_repository_counts = {}
    deployment_container_counts = {}
    deployments_missing_limits = []
    cpu_request_totals = 0
    cpu_request_count = 0
    env_name_counts = {}

    try:
        with open(manifest_file_path, 'r') as f:
            for manifest in yaml.safe_load_all(f):
                if manifest is None:
                    continue
                if not isinstance(manifest, dict):
                    continue

                kind = manifest.get("kind")
                metadata = manifest.get("metadata")
                spec = manifest.get("spec")
                if kind != "Deployment":
                    continue

                if not isinstance(metadata, dict) or not isinstance(spec, dict):
                    continue

                deployment_name = metadata.get("name")
                namespace = metadata.get("namespace", "default")
                replicas = spec.get("replicas")
                template = spec.get("template")
                pod_spec = template.get("spec")
                if not deployment_name:
                    continue

                results["deployment_count"] += 1
                namespace_counts[namespace] = namespace_counts.get(namespace, 0) + 1

                if not isinstance(template, dict):
                    continue

                if not isinstance(pod_spec, dict):
                    continue

                containers = pod_spec.get("containers")
                if not isinstance(containers, list):
                    containers = []

                node_selector = pod_spec.get("nodeSelector")
                if node_selector and isinstance(node_selector, dict):
                    results["deployments_with_node_selector"][deployment_name] = node_selector

                deployment_container_counts[deployment_name] = 0
                for container in containers:
                    if isinstance(container, dict):
                        deployment_container_counts[deployment_name] += 1

                for container in containers:
                    if not isinstance(container, dict):     
                        continue

                    container_name = container.get("name")
                    image = container.get("image")
                    resources = container.get("resources")
                    env = container.get("env")

                    if isinstance(image, str) and image:
                        repository = image.rsplit("/", 1)[-1]
                        repository = repository.split(":", 1)[0]
                        if repository:
                            image_repository_counts[repository] = image_repository_counts.get(repository, 0) + 1
 
                    if not isinstance(resources, dict):
                        resources = {}

                    requests = resources.get("requests")
                    limits = resources.get("limits")

                    if not isinstance(requests, dict):
                        requests ={}
                    if not isinstance(limits, dict):
                        limits ={}
                
                    if not limits and deployment_name not in deployments_missing_limits:
                        deployments_missing_limits.append(deployment_name)
                    
                    cpu_request = requests.get("cpu")
                    if isinstance(cpu_request, str) and cpu_request:
                        try:
                            if cpu_request.endswith("m"):
                                cpu_request = int(cpu_request[:-1]) # Remove the last character
                            else:
                                cpu_request = float(cpu_request) * 1000
                            cpu_request_totals += cpu_request
                            cpu_request_count += 1
                        except (ValueError, TypeError):
                            pass
                    
                    if not isinstance(env, list):
                        env = []
                    
                    for env_item in env:
                        if isinstance(env_item, dict):
                            env_name = env_item.get("name")
                            env_name_counts[env_name] = env_name_counts.get(env_name, 0) + 1
    

    except yaml.YAMLError:
        return results
    except FileNotFoundError:
        return results

    if deployment_container_counts:
        max_container_count = max(deployment_container_counts.values())
        results["largest_deployment_by_container_count"] = min({
            deployment_name_value 
            for deployment_name_value in deployment_container_counts
            if deployment_container_counts[deployment_name_value] == max_container_count
        })

    deployments_missing_limits.sort()
    results["deployments_missing_limits"] = deployments_missing_limits
    results["namespace_counts"] = namespace_counts
    results["env_name_counts"] = env_name_counts
    results["image_repository_counts"] = image_repository_counts
    if cpu_request_count > 0:
        average_cpu_request = cpu_request_totals / cpu_request_count
        results["average_cpu_request_millicores"] = round(average_cpu_request, 2)

    return results    


if __name__ == "__main__":
    manifest_file_path = "cluster_manifests.yaml"
    result = analyze_cluster_manifests(manifest_file_path)
    print(json.dumps(result, indent=4))