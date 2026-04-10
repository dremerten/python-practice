import json
import yaml


def triage_flaky_ci_run(yaml_file_path: str) -> dict:
    # ========================================================
    # 2) REQUIRED RETURN OBJECT
    # ========================================================
    results = {
        "classification": "unknown",
        "supporting_signal": None,
        "retry_recommended": False,
        "failed_job_name": None,
        "failed_step_name": None
    }

    # ========================================================
    # 3) HELPER STATE INITIALIZATION
    # ========================================================
    classification = "unknown"
    retry_recommended = False
    supporting_signal = None
    failed_job_name = None
    failed_step_name = None
    candidate_signals = []
    data = None

    # ========================================================
    # 4) FILE HANDLING RULES
    # ========================================================
    try:
        with open(yaml_file_path, "r") as f:
            data = yaml.safe_load(f)
    except FileNotFoundError:
        return results
    except yaml.YAMLError:
        return results

    # ========================================================
    # 5) ROOT VALIDATION RULES
    # ========================================================
    if not isinstance(data, dict):
        return results

    jobs = data.get("jobs")
    annotations = data.get("annotations", [])
    artifacts = data.get("artifacts", [])

    if not isinstance(jobs, list):
        return results
    if not isinstance(annotations, list):
        return results
    if not isinstance(artifacts, list):
        return results

    # ========================================================
    # 6) FAILURE TARGET SELECTION RULES
    # ========================================================
    selected_failed_step = None

    for job in jobs:
        if not isinstance(job, dict):
            continue

        job_name = job.get("name")
        job_conclusion = job.get("conclusion")
        steps = job.get("steps")

        if not isinstance(job_name, str):
            continue
        if not isinstance(job_conclusion, str):
            continue
        if not isinstance(steps, list):
            continue

        if job_conclusion == "failure":
            failed_job_name = job_name

            # ========================================================
            # 7) FAILED STEP SELECTION RULES
            # ========================================================
            for step in steps:
                if not isinstance(step, dict):
                    continue

                step_name = step.get("name")
                step_conclusion = step.get("conclusion")
                exit_code = step.get("exit_code")
                log_excerpt = step.get("log_excerpt")

                if not isinstance(step_name, str):
                    continue
                if not isinstance(step_conclusion, str):
                    continue
                if not isinstance(exit_code, int):
                    continue
                if not isinstance(log_excerpt, str):
                    continue

                if step_conclusion == "failure":
                    failed_step_name = step_name
                    selected_failed_step = step
                    break

            break

    if failed_job_name is None:
        return results

    # ========================================================
    # 8) SIGNAL COLLECTION RULES
    # ========================================================
    if isinstance(selected_failed_step, dict):
        log_excerpt = selected_failed_step.get("log_excerpt")
        normalized_excerpt = log_excerpt.lower()

        if (
            "secret" in normalized_excerpt
            or "credentials" in normalized_excerpt
            or "authentication failed" in normalized_excerpt
            or "access denied" in normalized_excerpt
            or "permission denied" in normalized_excerpt
        ):
            candidate_signals.append({
                "classification": "bad_secrets",
                "supporting_signal": log_excerpt,
                "retry_recommended": False,
                "priority": 1
            })

        elif (
            "docker pull" in normalized_excerpt
            or "pull access denied" in normalized_excerpt
            or "manifest unknown" in normalized_excerpt
            or "image not found" in normalized_excerpt
        ):
            candidate_signals.append({
                "classification": "bad_docker_pull",
                "supporting_signal": log_excerpt,
                "retry_recommended": False,
                "priority": 2
            })

        elif (
            "cache" in normalized_excerpt
            and (
                "corrupt" in normalized_excerpt
                or "checksum" in normalized_excerpt
                or "failed to extract" in normalized_excerpt
            )
        ):
            candidate_signals.append({
                "classification": "bad_cache",
                "supporting_signal": log_excerpt,
                "retry_recommended": True,
                "priority": 3
            })

        elif (
            "timeout" in normalized_excerpt
            or "connection reset" in normalized_excerpt
            or "tls handshake timeout" in normalized_excerpt
            or "temporary failure in name resolution" in normalized_excerpt
        ):
            candidate_signals.append({
                "classification": "infra_flakiness",
                "supporting_signal": log_excerpt,
                "retry_recommended": True,
                "priority": 4
            })

        elif (
            "assertion" in normalized_excerpt
            or "expected" in normalized_excerpt
            or "snapshot mismatch" in normalized_excerpt
            or "test failed" in normalized_excerpt
        ):
            candidate_signals.append({
                "classification": "test_flakiness",
                "supporting_signal": log_excerpt,
                "retry_recommended": True,
                "priority": 5
            })

        else:
            candidate_signals.append({
                "classification": "code_failure",
                "supporting_signal": log_excerpt,
                "retry_recommended": False,
                "priority": 50
            })

    for annotation in annotations:
        if not isinstance(annotation, dict):
            continue

        annotation_level = annotation.get("level")
        annotation_message = annotation.get("message")

        if not isinstance(annotation_level, str):
            continue
        if not isinstance(annotation_message, str):
            continue

        normalized_message = annotation_message.lower()

        if (
            "lost communication" in normalized_message
            or "runner disconnected" in normalized_message
            or "network error" in normalized_message
        ):
            candidate_signals.append({
                "classification": "infra_flakiness",
                "supporting_signal": annotation_message,
                "retry_recommended": True,
                "priority": 6
            })

    for artifact in artifacts:
        if not isinstance(artifact, dict):
            continue

        artifact_name = artifact.get("name")
        artifact_status = artifact.get("status")

        if not isinstance(artifact_name, str):
            continue
        if not isinstance(artifact_status, str):
            continue

        if artifact_name == "docker-layer-cache" and artifact_status != "available":
            candidate_signals.append({
                "classification": "bad_cache",
                "supporting_signal": f"{artifact_name} status: {artifact_status}",
                "retry_recommended": True,
                "priority": 7
            })

    # ========================================================
    # 9) FINAL SIGNAL SELECTION RULES
    # ========================================================
    if candidate_signals:
        candidate_signals.sort(key=lambda item: item["priority"])
        classification = candidate_signals[0]["classification"]
        supporting_signal = candidate_signals[0]["supporting_signal"]
        retry_recommended = candidate_signals[0]["retry_recommended"]

    # ========================================================
    # 10) FINAL ASSIGNMENT RULES
    # ========================================================
    results["classification"] = classification
    results["supporting_signal"] = supporting_signal
    results["retry_recommended"] = retry_recommended
    results["failed_job_name"] = failed_job_name
    results["failed_step_name"] = failed_step_name

    # ========================================================
    # 11) RETURN RULE
    # ========================================================
    return results


if __name__ == "__main__":
    yaml_file_path = "workflow_run_summary.yaml"
    result = triage_flaky_ci_run(yaml_file_path)
    print(json.dumps(result, indent=4))