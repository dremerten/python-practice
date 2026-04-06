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
        with open(file_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                try:
                    data = json.loads(line)
                except:
                    continue

                pipeline = data.get("pipeline")
                status = data.get("status")
                duration = data.get("duration")
                timestamp = data.get("timestamp")

                if not all((pipeline, status, timestamp)):
                    continue

                # pipeline_counts
                if pipeline not in results["pipeline_counts"]:
                    results["pipeline_counts"][pipeline] = 0
                results["pipeline_counts"][pipeline] += 1

                # status_counts
                if status not in results["status_counts"]:
                    results["status_counts"][status] = 0
                results["status_counts"][status] += 1

                # minute key
                if "T" not in timestamp:
                    continue
                date_part, time_part = timestamp.split("T")
                if ":" not in time_part:
                    continue
                hour, minute = time_part.split(":")[0:2]
                minute_key = f"{date_part} {hour}:{minute}"

                if minute_key not in minute_counts:
                    minute_counts[minute_key] = 0
                minute_counts[minute_key] += 1

                # failure tracking
                if status == "failed":
                    if pipeline not in pipeline_failure_counts:
                        pipeline_failure_counts[pipeline] = 0
                    pipeline_failure_counts[pipeline] += 1

                # success duration
                if status == "success":
                    if isinstance(duration, (int, float)):
                        success_duration_total += duration
                        success_count += 1

    except FileNotFoundError:
        return results

    # top_failed_pipeline
    if pipeline_failure_counts:
        max_fail = max(pipeline_failure_counts.values())
        candidates = []
        for p in pipeline_failure_counts:
            if pipeline_failure_counts[p] == max_fail:
                candidates.append(p)
        results["top_failed_pipeline"] = min(candidates)

    # frequent_failure_pipelines
    for p in pipeline_failure_counts:
        if pipeline_failure_counts[p] >= failure_threshold:
            results["frequent_failure_pipelines"][p] = pipeline_failure_counts[p]

    # busiest_minute
    if minute_counts:
        max_count = max(minute_counts.values())
        candidates = []
        for m in minute_counts:
            if minute_counts[m] == max_count:
                candidates.append(m)
        results["busiest_minute"] = min(candidates)

    # average_duration_success
    if success_count > 0:
        avg = success_duration_total / success_count
        results["average_duration_success"] = round(avg, 2)

    return results