'''
Your function must:

1. Load YAML from path (use yaml.safe_load)
2. Fail safely if:
    - File does not exist 
    - YAML is invalid
3. Ensure the loaded config is a dictionary
4. Ensure steps is a list if present (or raise a clear error)
5. Read environment variable ENV
6. If ENV matches a key under overrides:
7. Apply that override dict onto the base config using the same idea as update()
8. If the override includes steps, it replaces the entire steps list (no deep merge)
9. Do not mutate the original config dict
10. Remove overrides key before returning
11. Return the final config dict
'''