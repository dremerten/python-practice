import json

REQUIRED_KEYS = {
    "pipeline",
    "status",
    "duration",
    "timestamp"}


def analyze_pipeline_runs(file_path: str, slow_threshold_seconds: int = 900) -> dict:
    results = {
    "pipeline_counts": {},
    "status_counts": {},
    "top_failed_job": None,
    "slow_pipelines": {},
    "latest_prod_image_tag": None,
    "average_duration_seconds_successful_deploys": None,
    }

    pipeline_failure_counts = {}
    minute_counts = {}
    success_duration_total = 0
    success_count = 0

    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                try:
                    data = json.loads(line)
                except ValueError:
                    continue

                breakpoint()

    



        return results

    except FileNotFoundError:
        return results


if __name__ == "__main__":
    file_path = "pipeline_runs.jsonl"
    result = analyze_pipeline_runs(file_path)
    print(result)



