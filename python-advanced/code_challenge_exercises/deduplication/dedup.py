import json

with open('staging.json', 'r') as f:
    staging = json.load(f)

with open('production.json', 'r') as f:
    production = json.load(f)

staging_keys = staging.keys()
production_keys = production.keys()
intersetion_keys = set(staging_keys) & set(production_keys)

print(f"intersetion_keys are: {intersetion_keys}")

for service in intersetion_keys:
    staging_version = staging[service]
    prod_version = production[service]
    
    if staging_version != prod_version:
        print(f"   Mismatch found in {service}:")
        print(f"   Staging is at {staging_version}")
        print(f"   Production is at {prod_version}")
    else:
        print(f"{service} is in sync ({staging_version})")

