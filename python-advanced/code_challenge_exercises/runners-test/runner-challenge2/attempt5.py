import json
import os


def validate_runners(path: str) -> dict:
    results = {
        "usable": [],
        "rejected": {}
    }

    try:
        with open(path, 'r') as f:
            config = json.load(f)
            if not isinstance(config, dict):
                raise TypeError(f"{config} must be a dictionary, got {type(config).__name__}")
            
            runners = config.get("runners", {})
            if not isinstance(runners, list):
                raise TypeError(f"Runners must be a list, got {type(runners).__name__}")

            env = os.environ.get("ENV", "").lower().strip()
            default_min_disk_gb = 10

            overrides = config.get("overrides", {})
            if isinstance(overrides, dict) and env:
                env_overrides = overrides.get(env)
                if isinstance(env_overrides, dict):
                    min_disk_gb = env_overrides.get("min_disk_gb")
                    if min_disk_gb and not isinstance(min_disk_gb, int):
                        raise TypeError
                    default_min_disk_gb = min_disk_gb
            
            for runner in runners:
                if not isinstance(runner, dict):
                    continue

                name, online, disk_gb, tags = (
                    runner.get("name", "<unknown>"), 
                    runner.get("online", False),
                    runner.get("disk_gb", 0),
                    runner.get("tags", [])
                )

                if not isinstance(name, str):
                    name = "<unknown>"
                if not isinstance(online, bool):
                    online = False
                if not isinstance(disk_gb, (int, float)):
                    disk_gb = 0
                if not isinstance(tags, list):
                    tags = []

                if not online:
                    results["rejected"][name] = "Runner is offline"
                    continue

                if disk_gb < min_disk_gb:
                    results["rejected"][name] = "Insufficient disk space"
                    continue
                
                if "docker" not in tags:
                    results["rejected"][name] = "Missing required tag: 'docker'"
                
                results["usable"].append(name)
        return results
    
    except FileNotFoundError:
        return results
    
    except json.JSONDecodeError as e:
        print(f"{path} is invalid JSON - {e}") 
        return results

if __name__ == "__main__":
    path = "runners.json"
    result = validate_runners(path)
    print(json.dumps(result, indent=4))