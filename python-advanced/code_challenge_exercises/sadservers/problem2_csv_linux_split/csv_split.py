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
        with open(file_path, encoding="utf-8-sig") as f:
            reader = csv.reader(f)
            header = next(reader)

            for row in reader:
                line = [i.strip() for i in row]
                line = [i.partition("/")[0] for i in line]
                header = [i.partition("/")[0] for i in header]

                province = line[0].strip()
                electoral_district = line[1].strip().replace("--", " ")
                # electoral_district = electoral_district
                electoral_district_number = line[2].strip()
                candidate = line[3].strip()
                resisdence = line[4].strip()
                occupation = line[5].strip()
                votes = line[6].strip()
                
                province_count[province] = province_count.get(province, 0) + 1
                electoral_district_tracker[electoral_district] = electoral_district_tracker.setdefault(electoral_district, 0) + 1

                candidate_votes[candidate] = candidate_votes.get(candidate)
                candidate_votes[candidate] = votes

                candidate_occupation.add((candidate, occupation))
                #candidate_occupation[candidate] = candidate_occupation.setdefault(candidate, "") + occupation
                row_count += 1


               
    except FileNotFoundError:
        print(f"The file {file_path} could not be found or does not exist")

    results["Total Rows"] = row_count
    results["Provice Count"] = province_count
    results["Electoral District"] = electoral_district_tracker
    results["Candidate Occupation"] = sorted(candidate_occupation)

    return results

result = analyze_csv("data.csv")
print(json.dumps(result, indent=4, ensure_ascii=False))