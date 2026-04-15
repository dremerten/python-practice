"""
STUDENT GRADE REPORT — MID-LEVEL CHALLENGE

GOAL:
Read a CSV file containing student assessment data and produce
a structured summary report per student.

CSV format (comma-delimited, 8 columns):
    student_id, name, subject, grade, score, attempts, passed, enrollment_date

========================================================
DEPENDENCIES
--------------------------------------------------------
You will need to import: csv, json

The csv module is part of the standard library — no install needed.

To read a CSV file with headers use:
    csv.DictReader(f)

This returns each row as a dictionary where keys are the
column headers. This means you can access fields by name
instead of index — e.g. row["score"] instead of row[4].

========================================================
FUNCTION SIGNATURE
--------------------------------------------------------
process_student_grades(file_path: str) -> dict

Return shape:
    {
        total_students:       int
        subject_averages:     dict[str, float]
        top_performer:        str | None
        failed_students:      list[str]
        multi_attempt_students: dict[str, int]
    }

========================================================
TRACKING STATE
--------------------------------------------------------
Initialize your results dict with the return shape above.

Also initialize these helper structures outside the row loop:

    student_scores      dict[str, list[float]]  — collects all scores
                                                   per student for
                                                   final averaging

    subject_tracker     dict[str, list[float]]  — collects all scores
                                                   per subject for
                                                   final averaging

    student_attempts    dict[str, int]          — total attempts
                                                   accumulated per student

    failed_tracker      set()                   — student names who have
                                                   failed at least once;
                                                   using a set prevents
                                                   duplicates automatically

Note: total_students cannot be counted by just counting rows —
a student may appear multiple times across subjects. Think about
what makes a student unique in this dataset.

========================================================
FILE HANDLING
--------------------------------------------------------
Wrap everything in a try/except block.
    - Raise FileNotFoundError with a descriptive message
      if the file doesn't exist
    - Catch ValueError separately for bad data encountered
      during processing

========================================================
ROW PARSING
--------------------------------------------------------
Open the file with a context manager and pass the file
object to csv.DictReader. Iterate row by row.

For each row, strip whitespace from all values. A clean
pattern for this is:
    row = {k: v.strip() for k, v in row.items()}

Then extract your fields:
    student_id      — unique identifier
    name            — student's full name
    subject         — subject name
    grade           — letter grade e.g. "A", "B", "F"
    score           — numerical score, needs conversion to float
    attempts        — how many times attempted, needs conversion to int
    passed          — "True" or "False" string, needs conversion to bool
    enrollment_date — date string, keep as string

Skip the row if any required field is empty after stripping.

Type conversions — wrap in try/except, skip row on ValueError:
    score    -> float
    attempts -> int
    passed   -> passed == "True"   (converts string to bool)

========================================================
PER-ROW LOGIC
--------------------------------------------------------
With all fields validated and typed, update your state:

    student_scores      — append score to the list under this student's
                          name. Initialize the list if name isn't a
                          key yet.

    subject_tracker     — append score to the list under this subject.
                          Initialize the list if subject isn't a
                          key yet.

    student_attempts    — accumulate total attempts per student. Use
                          dict.get(name, 0) to retrieve their current
                          total (defaults to 0 if not seen yet), then
                          add the current row's attempts and assign
                          the result back under the same key.

                          End result: {"Bob": 5}

    failed_tracker      — if passed is False, add the student's name
                          to the set. Sets handle deduplication for you
                          so no need to check first.

========================================================
POST-LOOP COMPUTATION
--------------------------------------------------------
After all rows are processed, derive your final output fields:

    total_students          — len() on student_scores gives you the
                              unique student count since it has one
                              key per student.

    subject_averages        — iterate subject_tracker using .items() to
                              get each subject and its scores list.
                              Compute sum(scores) / len(scores) for each,
                              round to 2 decimals, and store in
                              results["subject_averages"] under the same
                              subject key.

    top_performer           — only compute if student_scores is non-empty.
                              Build a temporary dict called student_avgs
                              from student_scores using .items() to get
                              each name and its scores list. Compute
                              sum(scores) / len(scores) per student.
                              Then use max(student_avgs, key=student_avgs.get)
                              to find the top name and assign it to
                              results["top_performer"].

    failed_students         — convert failed_tracker to a sorted list
                              and store in results["failed_students"]

    multi_attempt_students  — iterate student_attempts using .items() to
                              get each name and total_attempts. Only
                              include students where total_attempts > 2;
                              store name and total_attempts in
                              results["multi_attempt_students"]

========================================================
EXPECTED OUTPUT
{
    "total_students": 10,
    "subject_averages": {
        "Math": 75.63,
        "Science": 72.98,
        "English": 72.25,
        "History": 72.87,
        "Art": 75.83
    },
    "top_performer": "Eva Martinez",
    "failed_students": [
        "Bob Smith",
        "Carol White",
        "David Brown",
        "Frank Lee",
        "Henry Davis",
        "Jack Taylor"
    ],
    "multi_attempt_students": {
        "Alice Johnson": 16,
        "Bob Smith": 25,
        "Carol White": 18,
        "David Brown": 36,
        "Eva Martinez": 15,
        "Frank Lee": 34,
        "Grace Kim": 15,
        "Henry Davis": 31,
        "Iris Wilson": 15,
        "Jack Taylor": 38
    }
}
"""