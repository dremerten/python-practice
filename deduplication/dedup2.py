import json

'''
1. Open and load json files
2. Get the keys for both staging and prod
3. Need to find the intersection -> find common/shared keys
4. The Goal: Find every service that exists in both files but has a different version number.



NOTES:
If you want to find...	            Use this Set Op	Terminology to use
All possible services	            A | B	Union
Services in both	                A & B	Intersection
Services ONLY in Staging	        A - B	Difference
Services NOT in both	            A ^ B	Symmetric Difference

'''

with open("staging.json", 'r') as f:
    staging = json.load(f)

with open("production.json", 'r') as f:
    production = json.load(f)

staging_keys = staging.keys()
production_keys = production.keys()
intersection_keys = set(staging_keys) & set(production_keys)

for service in intersection_keys:
    staging_version = staging[service]
    production_version = production[service]

    if staging_version != production_version:
        print(f"Mismatch in {service}")
        print(f"  Staging is at {staging_version}")
        print(f"  Prod is at {production_version}")
    else:
        print(f"Service {service} is in sync with {staging_version}")

