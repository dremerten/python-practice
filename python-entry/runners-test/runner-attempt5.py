import pprint

runners = [
    {"name": "runner-1", "online": True,  "disk_gb": 50, "tags": ["linux", "docker"]},
    {"name": "runner-2", "online": False, "disk_gb": 80, "tags": ["linux"]},
    {"name": "runner-3", "online": True,  "disk_gb": 5,  "tags": ["docker"]},
    {"name": "runner-4", "online": True,  "disk_gb": 20, "tags": []},
]

def validate_runners(runners: list) -> dict:
    usable = []
    rejected = {}

    for runner in runners:
        name = runner.get("name", "<unknown>")
        online = runner.get("online")
        disk_gb = runner.get("disk_gb", 0)
        tags = runner.get("tags", [])

        if not isinstance(name, str):
            raise TypeError(f"Value must be type str. Instead got: {type(name).__name__}")
        if not isinstance(online, bool):
            raise TypeError(f"Value must be type boolean. Instead got: {type(online).__name__}")
        if not isinstance(disk_gb, int):
            raise TypeError(f"Value must be type int. Instead got: {type(disk_gb).__name__}")
        if not isinstance(tags, list):
            raise TypeError(f"Value must be type list. Instead got: {type(tags).__name__} ")
        
        if not online:
            rejected[name] = "The runner is offline"
            continue
        if disk_gb < 10:
            rejected[name] = "The disk space is below threshold minimum"
            continue
        if "docker" not in tags:
            rejected[name] = "Missing required 'docker' tags"
            continue
        usable.append(name)
        
    return {
        "usable": usable,
        "rejected": rejected
    }

if __name__ == "__main__":
    runner = validate_runners(runners)
    pprint.pprint(runner, indent=4)


