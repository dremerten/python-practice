import csv
import json
from typing import Any


def analyze_support_tickets(csv_file: str) -> dict[str, Any]:
    results: dict[str, Any] = {
        "total_agents": 0,
        "team_average_resolution": {},
        "fastest_agent": None,
        "unsatisfied_agents": [],
        "repeat_reopen_agents": {}
    }

    agent_times = {}
    team_tracker = {}
    agent_reopens = {}
    unsatisfied_tracker =  set()

    try:
        with open(csv_file, 'r') as file:
            data = csv.DictReader(file)
            for row in data:
                if not row:
                    continue
                row = {k: v.strip() for k, v in row.items()}

                ticket_id = row.get("ticket_id")
                agent_name = row.get("agent_name")
                team = row.get("team")
                priority = row.get("priority") 
                resolution_minutes_str = row.get("resolution_minutes")
                reopened_count_str = row.get("reopened_count")
                satisfied = row.get("satisfied")
                channel = row.get("channel")
                created_date = row.get("created_date")
                
                required_fields = {ticket_id, agent_name, team, priority, resolution_minutes_str, reopened_count_str, satisfied, channel, created_date}
                if not all(required_fields):
                    continue
                
                try:
                    resolution_minutes = float(resolution_minutes_str)
                    reopened_count = int(reopened_count_str)
                    satisfied = satisfied == "True"
                except ValueError as err:
                    print(f"Value error occured: {err}")
                    continue

                agent_times.setdefault(agent_name, []).append(resolution_minutes)
                team_tracker.setdefault(team, []).append(resolution_minutes)
                agent_reopens[agent_name] = agent_reopens.get(agent_name, 0) + reopened_count
                
                if not satisfied:
                    unsatisfied_tracker.add(agent_name)
    except FileNotFoundError:
        print(f"The file {csv_file} could not be found or does not exist")
    except ValueError as err:
        print(f"An error occured while processing data: {err}")
        return results

    results["total_agents"] = len(agent_times)

    for team, minutes in team_tracker.items():
        results["team_average_resolution"][team] = round(sum(minutes) / len(minutes), 2)  

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
    print(json.dumps(output, indent=4))



