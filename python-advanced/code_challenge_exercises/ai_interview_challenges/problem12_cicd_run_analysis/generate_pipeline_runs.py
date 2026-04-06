import json
from datetime import datetime, timedelta

pipelines = ["build", "test", "deploy"]

rows = []
start_time = datetime(2026, 4, 4, 9, 0, 0)

# exact distribution to match expected results
success_target = 210
failed_target = 70
running_target = 20

success_count = 0
failed_count = 0
running_count = 0

for i in range(300):
    pipeline = pipelines[i % 3]

    # controlled status distribution
    if failed_count < 40 and pipeline == "deploy":
        status = "failed"
        failed_count += 1
    elif failed_count < 60 and pipeline == "test":
        status = "failed"
        failed_count += 1
    elif failed_count < 70:
        status = "failed"
        failed_count += 1
    elif running_count < 20:
        status = "running"
        running_count += 1
    else:
        status = "success"
        success_count += 1

    # duration only matters for success avg
    duration = 150 + (i % 100)

    timestamp = start_time + timedelta(minutes=i % 60)

    row = {
        "pipeline": pipeline,
        "status": status,
        "duration": duration,
        "timestamp": timestamp.strftime("%Y-%m-%dT%H:%M:%S")
    }

    rows.append(row)

with open("pipeline_runs.jsonl", "w") as f:
    for r in rows:
        f.write(json.dumps(r) + "\n")

print("Done. Lines written:", len(rows))