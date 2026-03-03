import json

staging_data = {
    "auth-service": "v2.1.0",
    "payment-gateway": "v1.4.2",
    "inventory-api": "v3.0.1",
    "frontend-app": "v5.2.0",
    "email-worker": "v1.0.5"
}

production_data = {
    "auth-service": "v2.0.5",
    "payment-gateway": "v1.4.2",
    "frontend-app": "v5.1.9",
    "database-proxy": "v1.0.0"
}

with open('staging.json', 'w') as f:
    json.dump(staging_data, f, indent=4)

with open('production.json', 'w') as f:
    json.dump(production_data, f, indent=4)

print("Files created: staging.json and production.json")