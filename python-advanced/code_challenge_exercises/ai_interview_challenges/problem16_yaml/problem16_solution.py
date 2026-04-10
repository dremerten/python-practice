import yaml
import json


def analyze_project_portfolio(yaml_file_path: str) -> dict:
    results = {
        "team_count": 0,
        "project_count": 0,
        "active_project_count": 0,
        "owner_task_counts": {},
        "priority_counts": {},
        "overdue_task_count": 0,
        "projects_missing_docs": [],
        "blocked_project_ids": [],
        "tag_counts": {},
        "highest_risk_project": {
            "project_id": None,
            "risk_score": None,
            "team_id": None
        },
        "average_tasks_per_project": None
    }

    owner_task_counts = {}
    priority_counts = {}
    tag_counts = {}
    projects_missing_docs = []
    blocked_project_ids = []
    total_task_count = 0
    project_count = 0
    active_project_count = 0
    overdue_task_count = 0
    team_count = 0

    highest_risk_candidates = []
    highest_risk_score = None

    try:
        with open(yaml_file_path, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)
    except FileNotFoundError:
        return results
    except yaml.YAMLError:
        return results

    if not isinstance(data, dict):
        return results

    snapshot_date = data.get("snapshot_date")
    teams = data.get("teams")

    if not isinstance(snapshot_date, str):
        return results

    if not isinstance(teams, list):
        return results

    for team in teams:
        if not isinstance(team, dict):
            continue

        team_id = team.get("team_id")
        projects = team.get("projects")

        if not isinstance(team_id, str):
            continue

        if not isinstance(projects, list):
            continue

        team_count += 1

        for project in projects:
            if not isinstance(project, dict):
                continue

            project_id = project.get("project_id")
            status = project.get("status")
            owner = project.get("owner")
            risk_score = project.get("risk_score")
            docs_url = project.get("docs_url")
            tags = project.get("tags")
            tasks = project.get("tasks")

            if not isinstance(project_id, str):
                continue

            if not isinstance(status, str):
                continue

            if not isinstance(owner, str):
                continue

            if not isinstance(risk_score, int):
                continue

            if not isinstance(tags, list):
                continue

            if not isinstance(tasks, list):
                continue

            if docs_url is not None and not isinstance(docs_url, str):
                continue

            project_count += 1

            if status == "active":
                active_project_count += 1

            if docs_url is None or docs_url == "":
                projects_missing_docs.append(project_id)

            for tag in tags:
                if not isinstance(tag, str):
                    continue

                if tag not in tag_counts:
                    tag_counts[tag] = 0

                tag_counts[tag] += 1

            if highest_risk_score is None or risk_score > highest_risk_score:
                highest_risk_score = risk_score
                highest_risk_candidates = [
                    {
                        "project_id": project_id,
                        "risk_score": risk_score,
                        "team_id": team_id
                    }
                ]
            elif risk_score == highest_risk_score:
                highest_risk_candidates.append(
                    {
                        "project_id": project_id,
                        "risk_score": risk_score,
                        "team_id": team_id
                    }
                )

            for task in tasks:
                if not isinstance(task, dict):
                    continue

                owner = task.get("owner")
                priority = task.get("priority")
                completed = task.get("completed")
                due_date = task.get("due_date")
                blocked = task.get("blocked")

                if not isinstance(owner, str):
                    continue

                if priority not in ["low", "medium", "high"]:
                    continue

                if not isinstance(completed, bool):
                    continue

                if not isinstance(due_date, str):
                    continue

                if not isinstance(blocked, bool):
                    continue

                total_task_count += 1

                if owner not in owner_task_counts:
                    owner_task_counts[owner] = 0

                owner_task_counts[owner] += 1

                if priority not in priority_counts:
                    priority_counts[priority] = 0

                priority_counts[priority] += 1

                if completed is False and due_date < snapshot_date:
                    overdue_task_count += 1

                if blocked is True and completed is False:
                    if project_id not in blocked_project_ids:
                        blocked_project_ids.append(project_id)

    results["team_count"] = team_count
    results["project_count"] = project_count
    results["active_project_count"] = active_project_count
    results["owner_task_counts"] = owner_task_counts
    results["priority_counts"] = priority_counts
    results["overdue_task_count"] = overdue_task_count
    results["tag_counts"] = tag_counts

    projects_missing_docs.sort()
    blocked_project_ids.sort()

    results["projects_missing_docs"] = projects_missing_docs
    results["blocked_project_ids"] = blocked_project_ids

    if highest_risk_candidates:
        highest_risk_candidates.sort(key=lambda item: item["project_id"])
        results["highest_risk_project"] = highest_risk_candidates[0]

    if project_count > 0:
        average_tasks_per_project = total_task_count / project_count
        average_tasks_per_project = round(average_tasks_per_project, 2)
        results["average_tasks_per_project"] = average_tasks_per_project

    return results

if __name__ == "__main__":
    yaml_file_path = "portfolio_snapshot.yaml"
    result = analyze_project_portfolio(yaml_file_path)
    print(json.dumps(result, indent=4))
