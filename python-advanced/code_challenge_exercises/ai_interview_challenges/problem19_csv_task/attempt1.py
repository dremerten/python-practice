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
        with open(file_path, 'r') as file:
            data = csv.DictReader(file)
            for row in data:

                row = {k: v.strip() for k, v in row.items()}
                student_id = row.get("student_id")
                name = row.get("name")
                subject = row.get("subject")
                grade = row.get("grade")
                score = row.get("score")
                attempts = row.get("attempts")
                passed = row.get("passed")
                enrollment_date = row.get("enrollment_date")

                required_fields = {student_id, name, subject, grade, score, attempts, passed, enrollment_date}
                if not all(required_fields):
                    continue

                try:
                    score = float(score)
                    attempts = int(attempts)
                    passed = passed == "True"
                except ValueError:
                    continue

                if name not in student_scores:
                    student_scores[name] = []
                student_scores[name].append(score)

                if subject not in subject_tracker:
                    subject_tracker[subject] = []
                subject_tracker[subject].append(score)

                student_attempts[name] = student_attempts.get(name, 0) + attempts

                if not passed:
                    failed_tracker.add(name)

    except FileNotFoundError:
        print(f"The file {file_path} can't be found or does not exist")
        return results
    except ValueError:
        return results

    results["total_students"] = len(student_scores)

    for subject, score in subject_tracker.items():
        average = sum(score) / len(score)
        results["subject_averages"][subject] = round(average, 2)

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