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

        if not isinstance(disk_gb, int):
            raise TypeError(
                f"The disk GB Storage must be an int. Instead got: {type(disk_gb).__name__}"
            )
        if not isinstance(tags, list):
            raise TypeError(
                f"The tags key must be a list. Instead got type {type(tags).__name__}"
            )

        if not online:
            rejected[name] = "runner is offline"
            continue

        if disk_gb < 10:
            rejected[name] = "insufficient disk space"
            continue

        if "docker" not in tags:
            rejected[name] = "missing docker tag"
            continue

        usable.append(name)

    return {
        "usable": usable,
        "rejected": rejected
    }


if __name__ == "__main__":
    runners = validate_runners(runners)
    pprint.pprint(runners, indent=4)
