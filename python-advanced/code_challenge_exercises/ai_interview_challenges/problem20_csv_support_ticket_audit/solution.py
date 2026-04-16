import csv
from typing import Any


def analyze_support_tickets(csv_file: str) -> dict[str, Any]:
    results: dict[str, Any] = {
        "total_agents": 0,
        "team_average_resolution": {},
        "fastest_agent": None,
        "unsatisfied_agents": [],
        "repeat_reopen_agents": {}
    }

    agent_times: dict[str, list[float]] = {}
    team_tracker: dict[str, list[float]] = {}
    agent_reopens: dict[str, int] = {}
    unsatisfied_tracker: set[str] = set()

    try:
        with open(csv_file, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                cleaned_row = {
                    key: value.strip() if isinstance(value, str) else value
                    for key, value in row.items()
                }

                ticket_id = cleaned_row.get("ticket_id", "")
                agent_name = cleaned_row.get("agent_name", "")
                team = cleaned_row.get("team", "")
                priority = cleaned_row.get("priority", "")
                resolution_minutes = cleaned_row.get("resolution_minutes", "")
                reopened_count = cleaned_row.get("reopened_count", "")
                satisfied = cleaned_row.get("satisfied", "")
                channel = cleaned_row.get("channel", "")
                created_date = cleaned_row.get("created_date", "")

                required_fields = [
                    ticket_id,
                    agent_name,
                    team,
                    priority,
                    resolution_minutes,
                    reopened_count,
                    satisfied,
                    channel,
                    created_date,
                ]

                if any(value == "" for value in required_fields):
                    continue

                try:
                    resolution_minutes = float(resolution_minutes)
                    reopened_count = int(reopened_count)
                    satisfied = satisfied.lower() == "yes"
                except ValueError:
                    continue

                if agent_name not in agent_times:
                    agent_times[agent_name] = []
                agent_times[agent_name].append(resolution_minutes)

                if team not in team_tracker:
                    team_tracker[team] = []
                team_tracker[team].append(resolution_minutes)

                agent_reopens[agent_name] = agent_reopens.get(agent_name, 0) + reopened_count

                if not satisfied:
                    unsatisfied_tracker.add(agent_name)

    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Could not open CSV file: {csv_file}") from exc
    except ValueError as exc:
        raise ValueError(f"Invalid data encountered while processing the CSV: {exc}") from exc

    results["total_agents"] = len(agent_times)

    results["team_average_resolution"] = {
        team: round(sum(times) / len(times), 2)
        for team, times in team_tracker.items()
    }

    if agent_times:
        agent_avg_times = {
            agent: sum(times) / len(times)
            for agent, times in agent_times.items()
        }
        results["fastest_agent"] = min(agent_avg_times, key=agent_avg_times.get)

    results["unsatisfied_agents"] = sorted(unsatisfied_tracker)

    results["repeat_reopen_agents"] = {
        agent: total_reopens
        for agent, total_reopens in agent_reopens.items()
        if total_reopens > 8
    }

    return results


if __name__ == "__main__":
    output = analyze_support_tickets("support_ticket_audit.csv")
    print(output)
