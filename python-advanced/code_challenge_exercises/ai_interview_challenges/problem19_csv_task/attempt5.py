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

    REQUIRED_FIELDS = (
        "student_id", 
        "name", 
        "subject", 
        "grade", 
        "score", 
        "attempts", 
        "passed", 
        "enrollment_date"
    )

    try:
        with open(file_path, mode='r', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                row = {k: v.strip() for k, v in row.items()}
                if not row:
                    continue
                student_id = row.get("student_id")
                name = row.get("name")
                subject = row.get("subject")
                grade = row.get("grade")
                score_str = row.get("score")
                attempts_str = row.get("attempts")
                passed_str = row.get("passed")
                enrollment_date = row.get("enrollment_date")
                try:
                    score = float(score_str)
                    attempts = int(attempts_str)
                    passed = passed_str == "True"
                except ValueError:
                    continue

                if not all(str(row.get(field, "")).strip() for field in REQUIRED_FIELDS):
                    continue

                student_scores.setdefault(name, []).append(score)
                subject_tracker.setdefault(subject, []).append(score)
                student_attempts[name] = student_attempts.get(name, 0) + attempts

                if passed == False:
                    failed_tracker.add(name)

    except ValueError:
        return results

    except FileNotFoundError:
        print(f"The file {file_path} can't be found or does not exist")

    results["total_students"] = len(student_scores)
    for subject, scores in subject_tracker.items():
        results["subject_averages"][subject] = round(sum(scores) / len(scores), 2)

    if student_scores:
         student_avgs = {
            name: sum(scores) / len(scores)
            for name, scores in student_scores.items()
    }
    results["top_performer"] = max(student_avgs, key=student_avgs.get)
    results["failed_students"] = sorted(failed_tracker)

    for name, total_attempts in student_attempts.items():
        if total_attempts > 2:
            results["multi_attempt_students"][name] = total_attempts


    return results


if __name__ == "__main__":
    result = process_student_grades("students.csv")
    print(json.dumps(result, indent=4))