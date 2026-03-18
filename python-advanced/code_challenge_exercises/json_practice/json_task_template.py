"""
Your function must:

def load_config(path: str) -> dict:

1. Load and parse the JSON file at `path`
   - Raise FileNotFoundError if the file does not exist
   - Raise ValueError if the file contains invalid JSON

2. Validate the top-level structure
   - The loaded data must be a dictionary, otherwise raise TypeError

3. Validate optional fields
   - "steps":
       * Default to an empty list if missing
       * Must be a list, otherwise raise TypeError
   - "allowed_ips":
       * Default to an empty list if missing
       * Must be a list, otherwise raise TypeError
       * Each element must be a string, otherwise raise TypeError

4. Validate overrides configuration
   - "overrides":
       * Default to an empty dictionary if missing
       * Must be a dictionary, otherwise raise TypeError

5. Determine active environment
   - Read ENV from environment variables
   - Normalize by stripping whitespace and converting to lowercase

6. Build the result configuration
   - Create a shallow copy of the base configuration to avoid mutation

7. Apply environment overrides (if applicable)
   - If ENV exists as a key in "overrides":
       * The override value must be a dictionary, otherwise raise TypeError
       * Merge it into the result using dict.update()
       * This replaces entire values (including lists like "steps" or "allowed_ips")

8. Finalize output
   - Remove the "overrides" key from the result only if an override was applied

9. Return the final configuration dictionary
"""