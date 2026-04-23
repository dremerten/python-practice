import json


def analyze_pipeline_runs(file_path: str, failure_threshold: int = 10) -> dict:
    results = {
    "pipeline_counts": {},
    "status_counts": {},
    "top_failed_pipeline": None,
    "frequent_failure_pipelines": {},
    "busiest_minute": None,
    "average_duration_success": None,
    }

    pipeline_failure_counts = {}
    minute_counts = {}
    success_duration_total = 0
    success_count = 0

    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                try:
                    data = json.loads(line)
                except ValueError:
                    continue

                required_keys = {key for key in data.keys()}
                missing_keys = required_keys - data.keys()
                if missing_keys:
                    print(f"Missing required key(s): {missing_keys}")
                    return results

                pipeline, status, duration, timestamp = (
                    data.get("pipeline"),
                    data.get("status"),
                    data.get("duration"),
                    data.get("timestamp")
                )

                if not pipeline or not status or not timestamp:
                    continue

                results["pipeline_counts"][pipeline] = results["pipeline_counts"].get(pipeline, 0) + 1
                results["status_counts"][status] = results["status_counts"].get(status, 0) + 1

                if "T" not in timestamp:
                    continue

                date_part, time_part = (
                    timestamp.split("T")[0], 
                    timestamp.split("T")[1]
                )

                if ":" not in timestamp:
                    continue

                time_parts = time_part.split(":")
                if len(time_parts) < 2:
                    continue

                hour, minute = time_parts[0], time_parts[1]
                minute_key = f"{date_part[:4]}-{date_part[5:7]}-{date_part[8:10]} {hour}:{minute}"
                minute_counts[minute_key] = minute_counts.get(minute_key, 0) + 1

                if status == "failed":
                    pipeline_failure_counts[pipeline] = pipeline_failure_counts.get(pipeline, 0) + 1

                if status == "success":
                    if isinstance(duration, (int, float)):
                        success_duration_total += duration
                        success_count += 1

    except FileNotFoundError:
        return results
    
    if pipeline_failure_counts:
        highest_failure_count = max(pipeline_failure_counts.values())
        results["top_failed_pipeline"] = min([
            pipeline_name
            for pipeline_name in pipeline_failure_counts
            if pipeline_failure_counts[pipeline_name] == highest_failure_count
        ])

    results["frequent_failure_pipelines"] = {
        pipeline_name: count
        for pipeline_name, count in pipeline_failure_counts.items()
        if pipeline_failure_counts[pipeline_name] >= failure_threshold
    }

    if minute_counts:
        highest_minute_count = max(minute_counts.values())
        results["busiest_minute"] = min([
            current_minute
            for current_minute in minute_counts
            if minute_counts[current_minute] == highest_minute_count
        ])

    
    if success_count > 0:
        average_duration = success_duration_total / success_count
        results["average_duration_success"] = round(average_duration, 2)
   
    return results

result = analyze_pipeline_runs("pipeline_runs.jsonl")
print(json.dumps(result, indent=4))