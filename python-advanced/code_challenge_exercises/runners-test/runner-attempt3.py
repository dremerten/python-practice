import pprint

runners = [
    {"name": "runner-1", "online": True,  "disk_gb": 50, "tags": ["linux", "docker"]},
    {"name": "runner-2", "online": False, "disk_gb": 80, "tags": ["linux"]},
    {"name": "runner-3", "online": True,  "disk_gb": 5,  "tags": ["docker"]},
    {"name": "runner-4", "online": True,  "disk_gb": 20, "tags": []},
]

def validate_runners(runners: list) -> dict:
    if not isinstance(runners, list):
        raise TypeError(
            f"The runners must be a type list. Instead got type {type(runners).__name__}"
            )
    usable = []
    rejected = {}

    for runner in runners:
        name = runner.get("name", "<unknown>")
        online = runner.get("online", False)
        disk_gb = runner.get("disk_gb", 0)
        tags = runner.get("tags", [])

        if not isinstance(runner, dict):
            raise TypeError(
                f"Runner must be a dictionary. Instead got {type(runner).__name__}"
                )
        if not isinstance(online, bool):
            raise TypeError(
                f"'Online' must be a boolean. Instead got: {type(online).__name__}"
                )
        if not isinstance(disk_gb, int):
            raise TypeError(
                f"'Disk_gb' must be a int. Instead got: {type(disk_gb).__name__}"
                )
        if not isinstance(tags, list):
            raise TypeError(
                f"'Tags' must be a list. Instead got: {type(tags).__name__}"
                )

        if not online:
            rejected[name] = "Runner is offline"
            continue
        if disk_gb < 10:
            rejected[name] = "Insuffient disk space"
            continue
        if "docker" not in tags:
            rejected[name] = "Missing tag: 'docker'"
            continue
        usable.append(name)

    return {
        "usable": usable,
        "rejected": rejected
    }

if __name__ == "__main__":
    runner = validate_runners(runners)
    pprint.pprint(runner, indent=4)

