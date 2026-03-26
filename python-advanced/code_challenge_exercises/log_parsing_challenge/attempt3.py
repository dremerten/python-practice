"""
SYSTEM LOG ANALYSIS — STEP-BY-STEP CHECKLIST

GOAL:
Read a log file line by line and:
- Count WARNING and ERROR logs per service
- Count ERROR message frequencies across all services
- Find the most common ERROR message (or None if no errors)

========================================================
1) FUNCTION SCAFFOLDING
--------------------------------------------------------
[ ] Define function: analyze_logs(path: str) -> dict
[ ] Initialize results dictionary with:
    {
        "service_counts": {},
        "error_messages": {},
        "most_common_error": None
    }

========================================================
2) FILE HANDLING
--------------------------------------------------------
[ ] Open file using: with open(path, "r") as f
[ ] Iterate line by line: for line in f
[ ] Strip whitespace: line = line.strip()
[ ] Skip empty lines

========================================================
3) SPLIT METADATA FROM MESSAGE
--------------------------------------------------------
Log format:
[timestamp] [service] [log_level] - message

[ ] Split line using: line.split(" - ", 1)
[ ] If split does NOT return 2 parts → skip line
[ ] meta = left side (strip whitespace)
[ ] message = right side (strip whitespace)

========================================================
4) PARSE METADATA (NO REGEX)
--------------------------------------------------------
Example meta:
[2026-03-01 14:22:10] [payments] [ERROR]

[ ] Split meta using: meta.split()
[ ] Expect at least 4 tokens (timestamp has a space)
[ ] If fewer than 4 tokens → skip line
[ ] Extract:
    - service token at index 2
    - log level token at index 3
[ ] Strip brackets using .strip("[]")
[ ] If service or log level is empty → skip line

========================================================
5) FILTER LOG LEVELS
--------------------------------------------------------
[ ] Only process log levels:
    - WARNING
    - ERROR
[ ] Ignore all other log levels (INFO, DEBUG, TRACE, etc.)

========================================================
6) UPDATE SERVICE COUNTS
--------------------------------------------------------
[ ] If service not in results["service_counts"]:
    initialize:
        {
            "ERROR": 0,
            "WARNING": 0
        }
[ ] Increment correct counter for the service

========================================================
7) TRACK ERROR MESSAGE FREQUENCIES
--------------------------------------------------------
[ ] Only for log level == "ERROR":
    - Increment results["error_messages"][message]
    - Use .get(message, 0) to avoid KeyError

========================================================
8) HANDLE MALFORMED LINES SAFELY
--------------------------------------------------------
[ ] Never crash on bad input
[ ] Skip lines that:
    - Don’t split correctly
    - Have fewer than 4 meta tokens
    - Have empty service or log level

========================================================
9) FIND MOST COMMON ERROR MESSAGE
--------------------------------------------------------
[ ] Initialize highest_count = 0
[ ] Iterate over results["error_messages"].items() **after reading the file**
[ ] For each (message, count):
    [ ] Compare count to highest_count
    [ ] If count is greater:
        [ ] Update results["most_common_error"] to this message
        [ ] Update highest_count to this count

========================================================
10) FINALIZE AND RETURN
--------------------------------------------------------
[ ] Return results dictionary

========================================================
EXPECTED RETURN STRUCTURE
--------------------------------------------------------
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
========================================================
"""

import pprint


def analyze_logs(PATH: str) -> dict:
    results = {
        "service_counts": {},
        "error_messages": {},
        "most_common_error": None
    }

    try:
        with open(PATH, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                parts = line.split(" - ")
                if len(parts) != 2:
                    continue

                meta, message = parts[0].strip(), parts[1].strip()
                meta = meta.split()
                if len(meta) < 4:
                    continue

                service, log_level = meta[2].strip("[]"), meta[3].strip("[]")
                if not (service and log_level):
                    continue

                if log_level.upper() in ("WARNING", "ERROR"):
                    if service not in results["service_counts"]:
                        results["service_counts"][service] =  {"ERROR": 0, "WARNING": 0}
                    results["service_counts"][service][log_level.upper()] += 1
                
                if log_level.upper() == "ERROR":
                    results["error_messages"][message] = results["error_messages"].get(message, 0) + 1

            # highest_count = 0
            # for message, count in results["error_messages"].items():
            #     if count > highest_count:
            #         results["most_common_error"] = message
            #         highest_count = count

            # better way to write the above code
            if results["error_messages"]:
                results["most_common_error"] = max(
                    results["error_messages"],
                    key=results["error_messages"].get
            )
                

    except FileNotFoundError as e:
        raise FileNotFoundError(
            f"The file at {PATH} does not exits or can't be found!"
            )


    return results

if __name__ == "__main__":
    PATH = "system.log"
    result = analyze_logs(PATH)
    pprint.pprint(result, indent=4)

#  # Calculate the most error-prone path (if any)
#         if results["path_error_counts"]:
#             # Find the path with the highest error count using max
#             results["top_error_path"] = max(results["path_error_counts"], key=results["path_error_counts"].get)
#         else:
#             results["top_error_path"] = None