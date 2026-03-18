"""
DEVOPS / INFRASTRUCTURE PYTHON INTERVIEW CHALLENGE
System Log Analyzer (No Regex — Built-in Python Only)

GOAL:
Implement analyze_logs(path: str) -> dict

The function should:
1. Count WARNING and ERROR logs per service
2. Count frequency of each ERROR message
3. Return the most common ERROR message (or None if no errors)

Assume consistent formatting.

Log Format Example:
##################################################################
<TimeStamp> <Service> <Log Level> - <Error Message>
##################################################################

[2026-03-01 14:22:10] [payments] [ERROR] - DB connection timed out
[2026-03-01 14:22:11] [auth] [WARNING] - Token refresh delay
[2026-03-01 14:22:12] [payments] [ERROR] - DB connection timed out

Expected Return Structure:
{
    "service_counts": {
        "payments": {"ERROR": 2, "WARNING": 0},
        "auth": {"ERROR": 0, "WARNING": 1}
    },
    "error_messages": {
        "DB connection timed out": 2
    },
    "most_common_error": "DB connection timed out"
}

Constraints:
- No regex
- Use basic string methods: split(), strip(), get()
- Do not crash on malformed input (skip safely)
"""


