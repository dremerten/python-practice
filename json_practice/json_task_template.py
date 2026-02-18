'''
Your function must:

def load_config(path: str) -> dict:

1. Load JSON from path using json.load
2. Fail safely if:
    - File doesn’t exist
    - JSON is invalid
3. Ensure the loaded config is a dictionary
4. If steps exists, ensure it is a list
5. If allowed_ips exists, ensure it is a list of strings
6. Read environment variable ENV
7. If ENV matches a key under overrides:
8. Apply the override dict to the base config (like update())
9. If the override includes steps or allowed_ips, it replaces the entire list
10. Do not mutate the original config dict
11. Remove overrides key before returning
12. Return the final config dict
'''