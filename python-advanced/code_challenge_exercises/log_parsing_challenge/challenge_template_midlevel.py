"""
SYSTEM LOG ANALYSIS — MID-LEVEL CHECKLIST

GOAL:
Read a log file line by line and:
- Populate results["service_counts"]
- Populate results["error_messages"]
- Set results["most_common_error"]

========================================================
1) FUNCTION SCAFFOLDING
--------------------------------------------------------
[ ] Define a function named analyze_logs that takes a file path and returns a dictionary
[ ] The file to be read is "system.log" located in the current working directory
[ ] Create a dictionary named results with:
    - results["service_counts"] = empty dictionary
    - results["error_messages"] = empty dictionary
    - results["most_common_error"] = None

========================================================
2) FILE HANDLING
--------------------------------------------------------
[ ] Open the file (system.log) using a context manager
[ ] Loop through the file one line at a time
[ ] Remove leading and trailing whitespace from each line - use .strip() string method
[ ] If the line is empty after stripping, skip to the next iteration - (if not line)

========================================================
3) SPLIT METADATA FROM MESSAGE
--------------------------------------------------------
Log format:

| ------------------------ parts -----------------------|
| --------- meta ---------------|  | ------ message ----|
[timestamp] [service] [log_level] - message

[ ] Split the line into two parts using " - " with a max of 1 split
[ ] If the result does not contain exactly 2 parts, skip the line
[ ] Assign:
    - meta = left part (strip whitespace)
    - message = right part (strip whitespace)

========================================================
4) PARSE METADATA 
--------------------------------------------------------
Example meta:
[2026-03-01 14:22:10] [payments] [ERROR]

[ ] Split meta into tokens using whitespace
[ ] If there are fewer than 4 tokens, skip the line
[ ] Extract:
    - service token at index 2
    - log level token at index 3
[ ] Remove "[" and "]" from both tokens
[ ] If service or log level is empty after stripping, skip the line

========================================================
5) FILTER LOG LEVELS
--------------------------------------------------------
[ ] Convert the extracted log level to uppercase
[ ] Compare the uppercase value to "WARNING" and "ERROR"
[ ] If it does not match either value, skip the line

========================================================
6) UPDATE SERVICE COUNTS
--------------------------------------------------------
[ ] Work inside results["service_counts"]
[ ] Check if the service exists as a key in results["service_counts"]
[ ] If it does NOT exist:
    [ ] Create:
        results["service_counts"][service] = {
            "ERROR": 0,
            "WARNING": 0
        }
[ ] Use the uppercase log level as the key
[ ] Increase results["service_counts"][service][log_level] by 1

========================================================
7) TRACK ERROR MESSAGE FREQUENCIES
--------------------------------------------------------
[ ] Only continue if log level is "ERROR"
[ ] Work inside results["error_messages"]
[ ] Check if message exists as a key in results["error_messages"]
[ ] If it does NOT exist:
    [ ] Set results["error_messages"][message] = 0
[ ] Increase results["error_messages"][message] by 1

========================================================
8) HANDLE MALFORMED LINES SAFELY
--------------------------------------------------------
[ ] At every step above:
    - If a required value is missing, skip the line
[ ] Do not allow index access unless length checks have passed
[ ] Continue processing remaining lines

========================================================
9) FIND MOST COMMON ERROR MESSAGE
--------------------------------------------------------
[ ] Check if results["error_messages"] is not empty
[ ] Find the key in results["error_messages"] with the highest value
[ ] Assign that key to results["most_common_error"]

========================================================
10) FINALIZE AND RETURN
--------------------------------------------------------
[ ] Return results
[ ] If results["error_messages"] is empty:
    - results["most_common_error"] remains None

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