import json
import yaml


def audit_docker_compose(file_path: str) -> dict:
    results = {
        "service_count": 0,
        "missing_restart_policy": [],
        "public_sensitive_ports": {},
        "unpinned_images": {},
        "shared_environment_variables": {},
        "undefined_dependencies": {}
    }

    # helpers
    env_usage = {}
    defined_services = set()
    sensitive_container_ports = {22, 2375, 2376, 3306, 5432, 6379, 27017}

    try:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
            if not isinstance(data, dict):
                print(f"The data is not a dictionary. Got {type(data).__name__}")
                return results
            
            services = data.get("services", {})
            if not isinstance(services, dict):
                print(f"Service must be a dictionary")
                return results
            
            results["service_count"] = len(services)
            defined_services = {i for i in services}

            for service_name, service_data in services.items():
                if not isinstance(service_data, dict):
                    continue

                image = service_data.get("image", "")
                ports = service_data.get("ports", [])
                environment = service_data.get("environment", [])
                depends_on = service_data.get("depends_on", [])
                restart = service_data.get("restart", None)

                if not isinstance(restart, str) or not restart:
                    results["missing_restart_policy"].append(service_name)

                if isinstance(image, str) and image:
                    if image.endswith(":latest") or ":" not in image:
                        results["unpinned_images"][service_name] = image

                if isinstance(ports, list):
                    for port in ports:
                        if not isinstance(port, str) or ":" not in port:
                            continue
                        host_port_str, container_port_str = port.split(":", 1)
                        try:
                            host_port = int(host_port_str)
                            container_port = int(container_port_str)
                        except ValueError:
                            continue
                        if host_port > 0 and container_port in sensitive_container_ports:
                            results["public_sensitive_ports"].setdefault(service_name, []).append((port, container_port))
                
                if isinstance(environment, list):
                    for env in environment:
                        if not isinstance(env, str) or "=" not in env:
                            continue
                        variable_name, _ = env.split("=", 1)
                        env_usage.setdefault(variable_name, set()).add(service_name)
                
                elif isinstance(environment, dict):
                    for variable_name in environment.keys():
                        if not isinstance(variable_name, str):
                            continue
                        env_usage.setdefault(variable_name, set()).add(service_name)

                missing_dependencies = []
                
                if isinstance(depends_on, list):
                    for dep_name in depends_on:
                        if not isinstance(dep_name, str):
                            continue
                        if dep_name not in defined_services:
                            missing_dependencies.append(dep_name)
                
                elif isinstance(depends_on, dict):
                    for dep_name in depends_on.keys():
                        if dep_name not in defined_services:
                            missing_dependencies.append(dep_name)
                
                if missing_dependencies:
                    results["undefined_dependencies"][service_name] = sorted(missing_dependencies)

        for variable_name, service_set in env_usage.items():
            if len(service_set) > 1:
                results["shared_environment_variables"][variable_name] = sorted(service_set)

        results["missing_restart_policy"].sort()

        for service_name, port_list in results["public_sensitive_ports"].items():
            port_list.sort()

        return results
                    
    except FileNotFoundError:
        print(f"The file {file_path} can not be found or does not exist")
        return results
    except yaml.YAMLError as err:
        print(f"The file is invalid YAML: {err}")
        return results
    except Exception as err:
        print(f"An unknown error has occured: {err}")
        return results


results = audit_docker_compose("docker-compose.yaml")
print(json.dumps(results, indent=4))