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
        pass



    return {
        "usable": usable,
        "rejected": rejected
    }


