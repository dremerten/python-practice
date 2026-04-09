import yaml
import json


def analyze_cluster_manifests(manifest_file_path: str) -> dict:
    # 2) REQUIRED RETURN OBJECT
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

    # 3) HELPER STATE INITIALIZATION
    namespace_counts = {}
    image_repository_counts = {}
    deployment_container_counts = {}
    deployments_missing_limits = []
    cpu_request_totals = 0
    cpu_request_count = 0
    env_name_counts = {}

    # 4) FILE HANDLING RULES
    try:
        with open(manifest_file_path, "r", encoding="utf-8") as file:
            for data in yaml.safe_load_all(file):
                # 4 B) Per-document handling
                if data is None:
                    continue
                if not isinstance(data, dict):
                    continue

                # 5) DOCUMENT VALIDATION RULES
                kind = data.get("kind")
                metadata = data.get("metadata")
                spec = data.get("spec")

                if kind != "Deployment":
                    continue
                if not isinstance(metadata, dict):
                    continue
                if not isinstance(spec, dict):
                    continue

                deployment_name = metadata.get("name")
                namespace = metadata.get("namespace")
                replicas = spec.get("replicas")
                template = spec.get("template")

                if not deployment_name:
                    continue
                if not namespace:
                    namespace = "default"

                # 5 E 1.
                results["deployment_count"] += 1

                # 5 E 2.
                if namespace not in namespace_counts:
                    namespace_counts[namespace] = 0
                namespace_counts[namespace] += 1

                # 6) NESTED POD SPEC EXTRACTION RULES
                if not isinstance(template, dict):
                    continue

                pod_spec = template.get("spec")
                if not isinstance(pod_spec, dict):
                    continue

                containers = pod_spec.get("containers")
                if not isinstance(containers, list):
                    containers = []

                node_selector = pod_spec.get("nodeSelector")
                if isinstance(node_selector, dict) and node_selector:
                    results["deployments_with_node_selector"][deployment_name] = node_selector

                deployment_container_counts[deployment_name] = 0
                for container in containers:
                    if isinstance(container, dict):
                        deployment_container_counts[deployment_name] += 1

                # 7) CONTAINER PARSING RULES
                for container in containers:
                    if not isinstance(container, dict):
                        continue

                    container_name = container.get("name")
                    image = container.get("image")
                    resources = container.get("resources")
                    env = container.get("env")

                    # 7 B) Image repository extraction
                    if isinstance(image, str) and image:
                        repository = image.rsplit("/", 1)[-1]
                        repository = repository.split(":", 1)[0]
                        if repository:
                            if repository not in image_repository_counts:
                                image_repository_counts[repository] = 0
                            image_repository_counts[repository] += 1

                    # 7 C) Resources handling
                    if not isinstance(resources, dict):
                        resources = {}

                    requests = resources.get("requests")
                    limits = resources.get("limits")

                    if not isinstance(requests, dict):
                        requests = {}
                    if not isinstance(limits, dict):
                        limits = {}

                    # 7 D) Missing limits tracking
                    if not limits and deployment_name not in deployments_missing_limits:
                        deployments_missing_limits.append(deployment_name)

                    # 7 E) CPU request tracking
                    cpu_request = requests.get("cpu")
                    if isinstance(cpu_request, str) and cpu_request:
                        try:
                            if cpu_request.endswith("m"):
                                cpu_request = int(cpu_request[:-1])
                            else:
                                cpu_request = float(cpu_request) * 1000
                            cpu_request_totals += cpu_request
                            cpu_request_count += 1
                        except (ValueError, TypeError):
                            pass

                    # 7 F) Environment variable tracking
                    if not isinstance(env, list):
                        env = []

                    for env_item in env:
                        if not isinstance(env_item, dict):
                            continue

                        env_name = env_item.get("name")
                        if isinstance(env_name, str) and env_name:
                            if env_name not in env_name_counts:
                                env_name_counts[env_name] = 0
                            env_name_counts[env_name] += 1

    except FileNotFoundError:
        return results
    except yaml.YAMLError:
        return results

    # 8 A) Compute largest_deployment_by_container_count
    if deployment_container_counts:
        max_container_count = max(deployment_container_counts.values())
        largest_deployment_candidates = []
        for deployment_name_value in deployment_container_counts:
            if deployment_container_counts[deployment_name_value] == max_container_count:
                largest_deployment_candidates.append(deployment_name_value)
        results["largest_deployment_by_container_count"] = min(largest_deployment_candidates)

    # 8 B) Final missing limits list handling
    deployments_missing_limits.sort()
    results["deployments_missing_limits"] = deployments_missing_limits

    # 8 C) Final namespace and image counts
    results["namespace_counts"] = namespace_counts
    results["image_repository_counts"] = image_repository_counts
    results["env_name_counts"] = env_name_counts

    # 8 D) Compute average_cpu_request_millicores
    if cpu_request_count > 0:
        average_cpu_request = cpu_request_totals / cpu_request_count
        results["average_cpu_request_millicores"] = round(average_cpu_request, 2)

    # 9) RETURN RULE
    return results

if __name__ == "__main__":
    manifest_file_path = "cluster_manifests.yaml"
    result = analyze_cluster_manifests(manifest_file_path)
    print(json.dumps(result, indent=4))
