import os

def apply_ci_overrides(config: dict) -> dict:
    ci_enabled = os.environ.get("CI", "").lower() == "true"

    # Always work on a copy to avoid mutation
    result = config.copy()

    if ci_enabled:
        overrides = config.get("ci_overrides", {})
        if isinstance(overrides, dict):
            result.update(overrides)

    # Remove internal key from final config
    result.pop("ci_overrides", None)

    return result

