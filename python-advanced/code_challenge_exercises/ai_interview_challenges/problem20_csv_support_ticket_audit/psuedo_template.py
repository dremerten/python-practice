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

    # 1. Import modules
    # 2. Define function with type hints
    # 3. Initialize results dict
    # 4. Initialize helper structures (agent_times, team_tracker, agent_reopens, unsatisfied_tracker)

    # 5. Open CSV file in try/except block
        # 6. Catch FileNotFoundError with descriptive message
        # 7. Catch ValueError for bad data during processing
        # 8. Wrap file in csv.DictReader to get rows as dictionaries

        # 9. Loop row by row
            # 10. Strip whitespace from all values in the row
            # 11. Extract all field values (ticket_id, agent_name, team, priority, resolution_minutes, reopened_count, satisfied, channel, created_date)
            # 12. Skip row if any required field is empty after stripping
            # 13. Convert types — resolution_minutes→float, reopened_count→int, satisfied→bool — skip row on ValueError
            # 14. Append resolution_minutes to agent_times[agent_name] list (initialize list first if needed)
            # 15. Append resolution_minutes to team_tracker[team] list (initialize list first if needed)
            # 16. Accumulate reopened_count into agent_reopens[agent_name] running total
            # 17. If satisfied is False, add agent_name to unsatisfied_tracker set

    # 18. Post-loop: compute total_agents from len(agent_times)
    # 19. Post-loop: compute team_average_resolution from team_tracker — sum/len per team, round to 2 decimals

    # 20. Post-loop: only compute fastest_agent if agent_times is non-empty
    # 21. Post-loop: build agent_avg_times dict — for each (agent, times) pair in agent_times.items(), compute sum(times) / len(times)
    # 22. Post-loop: find fastest_agent — min(agent_avg_times, key=agent_avg_times.get)

    # 23. Post-loop: convert unsatisfied_tracker set to a sorted list and store in results["unsatisfied_agents"]
    # 24. Post-loop: iterate agent_reopens.items() — for each (agent, total_reopens), if total_reopens > 8 store in results["repeat_reopen_agents"][agent]
    # 25. Return results

    return results


if __name__ == "__main__":
    output = analyze_support_tickets("support_ticket_audit.csv")
    print(output)


"""
CHALLENGE
Build a CSV analyzer for a customer support ticket log.

CSV COLUMNS
- ticket_id
- agent_name
- team
- priority
- resolution_minutes
- reopened_count
- satisfied
- channel
- created_date

RULES
- Skip rows with missing required fields after stripping whitespace.
- Skip rows where resolution_minutes or reopened_count cannot be converted.
- Treat satisfied as True only when the cleaned value is "yes" (case-insensitive).

RETURN FORMAT
{
    "total_agents": int,
    "team_average_resolution": dict[str, float],
    "fastest_agent": str | None,
    "unsatisfied_agents": list[str],
    "repeat_reopen_agents": dict[str, int]
}

EXPECTED OUTPUT FOR support_ticket_audit.csv
{
    "total_agents": 12,
    "team_average_resolution": {
        "Technical": 70.55,
        "Compliance": 67.21,
        "Retention": 56.21,
        "Onboarding": 55.33,
        "Billing": 56.34
    },
    "fastest_agent": "Lucas Reed",
    "unsatisfied_agents": [
        "Lucas Reed",
        "Maya Chen",
        "Nina Patel",
        "Owen Brooks",
        "Priya Shah",
        "Quinn Foster",
        "Ruby Nguyen",
        "Samir Ali",
        "Tessa Moore",
        "Victor Cruz",
        "Willa Scott",
        "Zane Cooper"
    ],
    "repeat_reopen_agents": {
        "Zane Cooper": 25,
        "Quinn Foster": 23,
        "Lucas Reed": 33,
        "Priya Shah": 19,
        "Owen Brooks": 26,
        "Willa Scott": 28,
        "Ruby Nguyen": 27,
        "Maya Chen": 36,
        "Samir Ali": 33,
        "Nina Patel": 12,
        "Victor Cruz": 23,
        "Tessa Moore": 13
    }
}
"""
