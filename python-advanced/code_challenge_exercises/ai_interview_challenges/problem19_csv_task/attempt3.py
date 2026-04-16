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
                if not isinstance(row, dict):
                    return results

                if not row:
                    continue

                student_id = row.get("student_id")
                name = row.get("name")
                subject = row.get("subject")
                grade = row.get("grade")
                score = row.get("score")
                attempts = row.get("attempts")
                passed = row.get("passed")
                enrollment_date = row.get("enrollment_date")

                if not any([
                    student_id, name, subject, 
                    grade, score, attempts, passed, 
                    enrollment_date 
                    ]):
                    continue
                
                try:
                    score = float(score)
                    attempts = int(attempts)
                    passed = passed == "True"
                except ValueError as err:
                    print(f"Skipping row due to conversion error: {err}")
                    continue
                
                student_scores.setdefault(name, []).append(score)

                subject_tracker.setdefault(subject, []).append(score)
                
                student_attempts.setdefault(name, 0)
                student_attempts[name] += attempts

                if not passed:
                    failed_tracker.add(name)
    except FileNotFoundError:
        print(f"File {file_path} can't be found or does not exist")
        return results
    except ValueError:
        print(f"File Level Error has occured")

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