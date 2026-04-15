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

    try:
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)

            for row in reader:
                # strip all values
                row = {k: v.strip() for k, v in row.items()}

                # extract fields
                student_id     = row.get("student_id", "")
                name           = row.get("name", "")
                subject        = row.get("subject", "")
                grade          = row.get("grade", "")
                score_str      = row.get("score", "")
                attempts_str   = row.get("attempts", "")
                passed_str     = row.get("passed", "")
                enrollment_date = row.get("enrollment_date", "")

                # skip if any required field is empty
                if not all([student_id, name, subject, grade,
                            score_str, attempts_str, passed_str]):
                    continue

                # type conversion
                try:
                    score    = float(score_str)
                    attempts = int(attempts_str)
                    passed   = passed_str == "True"
                except ValueError:
                    continue

                # student scores per name
                if name not in student_scores:
                    student_scores[name] = []
                student_scores[name].append(score)

                # subject scores
                if subject not in subject_tracker:
                    subject_tracker[subject] = []
                subject_tracker[subject].append(score)

                # attempts accumulation
                student_attempts[name] = student_attempts.get(name, 0) + attempts

                # failed tracker
                if not passed:
                    failed_tracker.add(name)

    except FileNotFoundError:
        raise FileNotFoundError(
            f"The file at '{file_path}' does not exist or cannot be found."
        )

    # total unique students
    results["total_students"] = len(student_scores)

    # subject averages
    for subject, scores in subject_tracker.items():
        results["subject_averages"][subject] = round(sum(scores) / len(scores), 2)

    # top performer
    if student_scores:
        student_avgs = {
            name: sum(scores) / len(scores)
            for name, scores in student_scores.items()
        }
        results["top_performer"] = max(student_avgs, key=student_avgs.get)

    # failed students
    results["failed_students"] = sorted(failed_tracker)

    # multi attempt students
    for name, total_attempts in student_attempts.items():
        if total_attempts > 2:
            results["multi_attempt_students"][name] = total_attempts

    return results


if __name__ == "__main__":
    result = process_student_grades("students.csv")
    print(json.dumps(result, indent=4))