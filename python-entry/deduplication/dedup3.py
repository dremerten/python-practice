import json

'''

Now, write a script to read these files and identify the version mismatches.

The Goal: Find every service that exists in both files but has a different version number.


1. Open and load json files
2. Get the keys for both staging and prod
3. Need to find the intersection -> find common/shared keys
4. The Goal: Find every service that exists in both files but has a different version number.
5. for loop (services or intersection keys)
6. if/else staging != prod



NOTES:
If you want to find...	            Use this Set Op	Terminology to use
All possible services	            A | B	Union
Services in both	                A & B	Intersection
Services ONLY in Staging	        A - B	Difference
Services NOT in both	            A ^ B	Symmetric Difference

'''
import json

with open("staging.json", 'r') as f:
    staging = json.load(f)

with open("production.json", 'r') as f:
    production = json.load(f)

staging_keys = staging.keys()
production_keys = production.keys()
intersection_keys = set(staging_keys) & set(production_keys)
print(intersection_keys)

for service in intersection_keys:
    staging_service = staging[service]
    production_service = production[service]

    if staging_service != production_service:
        print(f"Mismatch in {service}:")
        print(f"  Staging is running version: {staging_service}")
        print(f"  Production is running version: {production_service}")
    else:
        print(f"Both Environments match for service: {service} running {staging_service}")