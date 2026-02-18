runners = [
    {"name": "runner-1", "disk_gb": 50, "online": True},
    {"name": "runner-2", "disk_gb": 5, "online": True},
    {"name": "runner-3", "disk_gb": 100, "online": False}
]


def validate_runners(runners):
    usable = []
    rejected = {}

    for runner in runners:
        if not runner["online"]:
            rejected[runner["name"]] = "offline"
        elif runner["disk_gb"] < 10:
            rejected[runner["name"]] = "insufficient disk"
        else:
            usable.append(runner["name"])

    return {
        "usable": usable,
        "rejected": rejected
    }

if __name__ == "__main__":
    result = validate_runners(runners)
    print(result)