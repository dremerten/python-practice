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
        online = runner.get("online", False)
        disk_gb = runner.get("disk_gb", 0)
        tags = runner.get("tags", [])

        if not isinstance(online, bool):
            raise TypeError(
                f"Online status must be a boolean {online}"
                )
        if not isinstance(disk_gb, int):
            raise TypeError(
                f"The disk gb must be an int"
                )
        if not isinstance(tags, list):
            raise TypeError(f"Must be a list {tags}")

        if not online:
            rejected[name] = "Instance is not online"
            continue
        if disk_gb < 10:
            rejected[name] = "The disk space is insuffient"
            continue
        if "docker" not in tags:
            rejected[name] = "Missing the 'docker' tag"
            continue
        usable.append(name)
        

    return {
        "usable": usable,
        "rejected": rejected
    }

if __name__ == "__main__":
    runner = validate_runners(runners)
    pprint.pprint(runner, indent=4)



