"""
Your function must:

1. Load a YAML file from a given path using yaml.safe_load

2. Raise a clear FileNotFoundError if the file does not exist

3. Raise a clear yaml.YAMLError if the YAML content is invalid

4. Ensure the loaded config is a dictionary
   - If not, raise a TypeError

5. Extract "steps" and "overrides" from the config
   - "steps" must be a list if it is not None
   - If "steps" is not a list, raise a TypeError

6. Read the ENV environment variable
   - Normalize it by stripping whitespace and converting to lowercase

7. Create a shallow copy of the config (do not mutate the original)

8. If ENV exists as a key inside "overrides":
   - Retrieve the corresponding override dictionary
   - Apply it to the copied config using dict.update()

9. Do not perform any deep merging
   - If "steps" exists in overrides, it replaces the original value entirely

10. Remove the "overrides" key from the final result

11. Return the final configuration dictionary
"""