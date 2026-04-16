"""
# 1. Import modules
# 2. Define function with type hints
# 3. Initialize results dict
# 4. Initialize helper structures (student_scores, subject_tracker, student_attempts, failed_tracker)

# 5. Open CSV file in try/except block
    # 6. Catch FileNotFoundError with descriptive message
    # 7. Catch ValueError for bad data during processing
    # 8. Wrap file in csv.DictReader to get rows as dictionaries

    # 9. Loop row by row
        # 10. Strip whitespace from all values in the row
        # 11. Extract all field values (student_id, name, subject, grade, score, attempts, passed, enrollment_date)
        # 12. Skip row if any required field is empty after stripping
        # 13. Convert types — score→float, attempts→int, passed→bool — skip row on ValueError
        # 14. Append score to student_scores[name] list (initialize list first if name not yet a key)
        # 15. Append score to subject_tracker[subject] list (initialize list first if subject not yet a key)
        # 16. Accumulate attempts into student_attempts[name] running total (use .get(name, 0) + attempts)
        # 17. If passed is False, add student name to failed_tracker set

# 18. Post-loop: compute total_students from len(student_scores)
# 19. Post-loop: compute subject_averages from subject_tracker — sum/len per subject, round to 2 decimals

# 20. Post-loop: only compute top_performer if student_scores is non-empty (if student_scores:)
# 21. Post-loop: build student_avgs dict — for each (name, scores) pair in student_scores.items(), compute sum(scores) / len(scores)
# 22. Post-loop: find top_performer — max(student_avgs, key=student_avgs.get) iterates student_avgs keys (names), and for each key uses student_avgs.get to look up its average as the comparison value, returning the name with the highest average

# 21. Post-loop: convert failed_tracker set to a sorted list and store in results["failed_students"]
# 22. Post-loop: iterate student_attempts.items() — for each (name, total_attempts), if total_attempts > 2 store in results["multi_attempt_students"][name]
# 23. Return results

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