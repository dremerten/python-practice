import csv
import json


def analyze_csv(file_path: str):
    results = {
        "Total Rows": None,
        "Provice Count": {},
        "Electoral Counts By District": {},
        "Candidate Occupation": []
    }

    row_count = 0
    province_count = {}
    electoral_district_tracker = {}
    candidate_votes = {}
    candidate_occupation = set()

    try:
        with open(file_path, 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            header = next(reader)
            header = {k: v.strip() for k, v in header.items()}
            breakpoint()
    except FileNotFoundError:
        print(f"The file {file_path} can't be found or does not exist")


    return results

result = analyze_csv("data.csv")
print(json.dumps(result, indent=4, ensure_ascii=False))