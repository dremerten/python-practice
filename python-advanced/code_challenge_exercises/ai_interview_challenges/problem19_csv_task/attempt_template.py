import csv
import json


def process_student_grades(file_path: str) -> dict:
    results = {
        "total_students": 0,
        "subject_averages": {},
        "top_performer": None,
        "failed_students": [],
        "multi_attempt_students": {}
    }

    # helpers
    student_scores = {}
    subject_tracker = {}
    student_attempts = {}
    failed_tracker = set()


    return results


if __name__ == "__main__":
    result = process_student_grades("students.csv")
    print(json.dumps(result, indent=4))