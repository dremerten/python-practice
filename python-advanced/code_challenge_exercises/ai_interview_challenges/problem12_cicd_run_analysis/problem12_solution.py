import json
from pprint import pprint


# 1)

def analyze_pipeline_runs(file_path: str, failure_threshold: int = 10) -> dict:
    
    # 2)
    results = {
    "pipeline_counts": {},
    "status_counts": {},
    "top_failed_pipeline": None,
    "frequent_failure_pipelines": {},
    "busiest_minute": None,
    "average_duration_success": None,
    }

    # 3)
    pipeline_failure_counts = {}
    minute_counts = {}
    success_duration_total = 0
    success_count = 0

    # 4)
    try:
        with open(file_path, 'r') as f:
            # 5)
            for line in f:
                line = line.strip() # str
                if not line:
                    continue

                try:
                    data = json.loads(line) # dict
                except ValueError:
                    continue
                
                # 6 A)
                pipeline = data.get("pipeline")
                status = data.get("status")
                duration = data.get("duration")
                timestamp = data.get("timestamp")

                # 6 B)
                if not all((pipeline, status, timestamp)):
                    continue

                # 6 C - 1 & 2)
                results["pipeline_counts"][pipeline] = results["pipeline_counts"].get(pipeline, 0) + 1
                results["status_counts"][status] = results["status_counts"].get(status, 0) + 1

                # 6 D)
                if "T" not in timestamp:
                    continue

                date_part, time_part = timestamp.split("T")
                if ":" not in time_part:
                    continue

                time_parts = time_part.split(":")
                if len(time_parts) < 2:
                    continue

                hour = time_parts[0]
                minute = time_parts[1]
                minute_key = f"{date_part} {hour}:{minute}"

                # 6 E)
                minute_counts[minute_key] = minute_counts.get(minute_key, 0) + 1

                # 6 F)
                if status == "failed":
                    pipeline_failure_counts[pipeline] = pipeline_failure_counts.get(pipeline, 0) + 1
                
                # 6 G)
                if status == "success":
                    if isinstance(duration, int) or isinstance(duration, float):
                        success_duration_total += duration
                        success_count += 1
                
    except FileNotFoundError:
        return results
    
    # 7 A)
    if pipeline_failure_counts:
        highest_failure_count = max(pipeline_failure_counts.values())
        results["top_failed_pipeline"] = min([
            pipeline_name
            for pipeline_name in pipeline_failure_counts
            if pipeline_failure_counts[pipeline_name] == highest_failure_count
        ])

    # 7 B)
    results["frequent_failure_pipelines"] = {
        pipeline_name: count
        for pipeline_name, count in pipeline_failure_counts.items()
        if pipeline_failure_counts[pipeline_name] >= failure_threshold
    }

    # 7 C)
    if minute_counts:
        highest_minute_count = max(minute_counts.values())
        results["busiest_minute"] = min([
            current_minute
            for current_minute in minute_counts
            if minute_counts[current_minute] == highest_minute_count
        ])

    # 7 D)
    if success_count > 0:
        average_duration = success_duration_total / success_count
        results["average_duration_success"] = round(average_duration, 2)
    
    # 8)
    return results


if __name__ == "__main__":
    file_path = "pipeline_runs.jsonl"
    result = analyze_pipeline_runs(file_path)
    pprint(result)



