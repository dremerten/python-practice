"""
CODE CHALLENGE: System Log Analysis (No Regex)

You are given a system log file where each line follows this format:

    [timestamp] [service] [log_level] - [message]

Example:
    [2026-02-10 09:00:05] [api] [WARNING] - Token is about to expire
    [2026-02-10 09:00:11] [auth] [ERROR] - Server unavailable

LOG LEVELS:
    INFO, DEBUG, WARNING, ERROR, TRACE

TASK:

Write a function that reads the log file and returns a dictionary
with the following information:

1. A count of log entries per log level.
2. The most frequent WARNING message.
3. The most frequent ERROR message.

FUNCTION SIGNATURE:

    def analyze_logs(path: str) -> dict:

EXPECTED RETURN FORMAT:

    {
        "level_counts": {
            "INFO": int,
            "DEBUG": int,
            "WARNING": int,
            "ERROR": int,
            "TRACE": int
        },
        "most_common_warning": str | None,
        "most_common_error": str | None
    }

CONSTRAINTS:

- Use Python 3
- Do NOT use regular expressions
- Use basic string operations only (split, strip)
- Read the file line by line (do not load entire file into memory)
- Handle malformed or unexpected lines safely

BONUS (OPTIONAL):

- Write clean, readable code
- Explain your approach step by step
- Add a simple unit test

"""
import pprint


def analyze_logs(path):
    error_count = 0
    warning_count = 0
    error_messages = {}
    warning_messages = {}

    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or " - " not in line:
                continue
            meta, message = line.split(" - ", 1)
            level = meta.rsplit(" ", 1)[-1].strip("[]")

            if level == "ERROR":
                error_count += 1
                error_messages[message] = error_messages.get(message, 0) + 1

            elif level == "WARNING":
                warning_count += 1
                warning_messages[message] = warning_messages.get(message, 0) + 1

    def most_common(messages):
        top = None
        top_count = 0
        for msg, count in messages.items():
            if count > top_count:
                top = msg
                top_count = count
        return top

    return {
        "error_count": error_count,
        "warning_count": warning_count,
        "most_common_error": most_common(error_messages),
        "most_common_warning": most_common(warning_messages),
    }



result = analyze_logs("/home/andre/DevOps-Practice/python-practice/log_parsing_challenge/system.log")
pprint.pprint(result, indent=4)
