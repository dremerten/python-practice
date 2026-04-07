import json
import random
from datetime import datetime, timedelta

random.seed(42)

rows = []
start_time = datetime(2026, 4, 4, 9, 0, 0)

pipeline_weights = [
    ("build", 0.42),
    ("test", 0.33),
    ("deploy", 0.25),
]

status_weights = {
    "build": [("success", 0.78), ("failed", 0.16), ("running", 0.06)],
    "test": [("success", 0.70), ("failed", 0.22), ("running", 0.08)],
    "deploy": [("success", 0.62), ("failed", 0.28), ("running", 0.10)],
}

minute_offsets = []

# normal activity
for _ in range(220):
    minute_offsets.append(random.randint(0, 179))

# burst around 09:28
for _ in range(35):
    minute_offsets.append(28)

# smaller burst around 10:12
for _ in range(20):
    minute_offsets.append(72)

# smaller burst around 11:05
for _ in range(25):
    minute_offsets.append(125)

random.shuffle(minute_offsets)

def weighted_choice(weighted_values):
    roll = random.random()
    running_total = 0.0
    for value, weight in weighted_values:
        running_total += weight
        if roll <= running_total:
            return value
    return weighted_values[-1][0]

def generate_duration(pipeline, status):
    if status == "running":
        return random.randint(60, 400)

    if pipeline == "build":
        if status == "success":
            return random.randint(180, 420)
        return random.randint(200, 500)

    if pipeline == "test":
        if status == "success":
            return random.randint(120, 360)
        return random.randint(150, 420)

    if pipeline == "deploy":
        if status == "success":
            return random.randint(240, 720)
        return random.randint(300, 900)

    return random.randint(100, 300)

for index in range(300):
    pipeline = weighted_choice(pipeline_weights)
    status = weighted_choice(status_weights[pipeline])
    duration = generate_duration(pipeline, status)

    timestamp = start_time + timedelta(
        minutes=minute_offsets[index],
        seconds=random.randint(0, 59),
    )

    row = {
        "pipeline": pipeline,
        "status": status,
        "duration": duration,
        "timestamp": timestamp.strftime("%Y-%m-%dT%H:%M:%S"),
    }

    rows.append(row)

with open("pipeline_runs.jsonl", "w") as file_handle:
    for row in rows:
        file_handle.write(json.dumps(row) + "\n")

print("Done. Lines written:", len(rows))