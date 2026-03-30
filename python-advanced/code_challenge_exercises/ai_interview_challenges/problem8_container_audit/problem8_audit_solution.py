import yaml


def audit_docker_compose(file_path: str) -> dict:
    results = {
        "service_count": 0,
        "missing_restart_policy": [],
        "public_sensitive_ports": {},
        "unpinned_images": {},
        "shared_environment_variables": {},
        "undefined_dependencies": {},
    }

    env_usage = {}
    defined_services = set()
    sensitive_container_ports = {22, 2375, 2376, 3306, 5432, 6379, 27017}

    try:
        with open(file_path, "r") as file:
            data = yaml.safe_load(file)

        if not isinstance(data, dict):
            print("Error: Top-level YAML must be a dictionary.")
            return results

        services = data.get("services", {})

        if not isinstance(services, dict):
            return results

        results["service_count"] = len(services)
        defined_services = set(services.keys())

        for service_name, service_data in services.items():
            if not isinstance(service_data, dict):
                continue

            image = service_data.get("image", "")
            ports = service_data.get("ports", [])
            environment = service_data.get("environment", [])
            depends_on = service_data.get("depends_on", [])
            restart = service_data.get("restart", None)

            if not restart or not isinstance(restart, str):
                results["missing_restart_policy"].append(service_name)

            if isinstance(image, str) and image:
                if image.endswith(":latest") or ":" not in image:
                    results["unpinned_images"][service_name] = image

            if isinstance(ports, list):
                for port_entry in ports:
                    if not isinstance(port_entry, str):
                        continue

                    if ":" not in port_entry:
                        continue

                    host_part, container_part = port_entry.split(":", 1)

                    try:
                        host_port = int(host_part)
                        container_port = int(container_part)
                    except ValueError:
                        continue

                    if host_port > 0 and container_port in sensitive_container_ports:
                        results["public_sensitive_ports"].setdefault(service_name, [])
                        results["public_sensitive_ports"][service_name].append(
                            (port_entry, container_port)
                        )

            if isinstance(environment, list):
                for item in environment:
                    if not isinstance(item, str):
                        continue

                    if "=" not in item:
                        continue

                    variable_name, _ = item.split("=", 1)
                    env_usage.setdefault(variable_name, set())
                    env_usage[variable_name].add(service_name)

            elif isinstance(environment, dict):
                for variable_name in environment.keys():
                    if not isinstance(variable_name, str):
                        continue

                    env_usage.setdefault(variable_name, set())
                    env_usage[variable_name].add(service_name)

            missing_dependencies = []

            if isinstance(depends_on, list):
                for dependency_name in depends_on:
                    if not isinstance(dependency_name, str):
                        continue

                    if dependency_name not in defined_services:
                        missing_dependencies.append(dependency_name)

            elif isinstance(depends_on, dict):
                for dependency_name in depends_on.keys():
                    if dependency_name not in defined_services:
                        missing_dependencies.append(dependency_name)

            if missing_dependencies:
                results["undefined_dependencies"][service_name] = sorted(
                    missing_dependencies
                )

        for variable_name, service_set in env_usage.items():
            if len(service_set) > 1:
                results["shared_environment_variables"][variable_name] = sorted(
                    service_set
                )

        results["missing_restart_policy"].sort()

        for service_name in results["public_sensitive_ports"]:
            results["public_sensitive_ports"][service_name].sort()

        return results

    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
        return results
    except yaml.YAMLError as error:
        print(f"Error: Invalid YAML: {error}")
        return results
    except Exception as error:
        print(f"Error: {error}")
        return results


if __name__ == "__main__":
    sample_file_path = "docker-compose.yml"
    audit_results = audit_docker_compose(sample_file_path)
    print(audit_results)