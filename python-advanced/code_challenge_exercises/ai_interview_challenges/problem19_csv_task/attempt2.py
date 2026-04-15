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
                enrollment_data = row.get("enrollment_data")

                required_fields = {
                    student_id,
                    name,
                    subject,
                    grade,
                    score, 
                    attempts, 
                    passed, 
                    enrollment_data,

                }
                if not any(required_fields):
                    continue

                try:
                    score = float(score)
                    attempts = int(attempts)
                    passed = passed == "True"
                except ValueError:
                    continue
                
                # if name not in student_scores:
                #     student_scores[name] = []
                # student_scores[name].append(score)
                student_scores.setdefault(name, []).append(score)

                subject_tracker.setdefault(subject, []).append(score)
                student_attempts[name] =  student_attempts.get(name, 0) + attempts

                if not passed:
                    failed_tracker.add(name)

    except FileNotFoundError:
        print(f"File {file_path} could not be found or does not exits")
        return results
    except ValueError as e:
        raise ValueError(f"Invalid error: {e}") from e

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
    breakpoint()

    return results


if __name__ == "__main__":
    result = process_student_grades("students.csv")
    print(json.dumps(result, indent=4))