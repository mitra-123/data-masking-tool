import yaml
from masking.exceptions import MaskingConfigError

def load_config(path: str) -> dict:
    try:
        with open(path, "r") as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        raise MaskingConfigError(f"Config file not found: {path}")
    except yaml.YAMLError as e:
        raise MaskingConfigError(f"Invalid YAML in config: {e}")

    if "fields" not in config:
        raise MaskingConfigError("Config missing required key: 'fields'")

    if not isinstance(config["fields"], dict):
        raise MaskingConfigError("'fields' must be a mapping of field names to strategies")

    return config

def validate_config(path: str, strategy_map: dict) -> list[str]:
    errors = []
    try:
        config = load_config(path)
    except MaskingConfigError as e:
        return [str(e)]

    for field, options in config["fields"].items():
        if "strategy" not in options:
            errors.append(f"Field '{field}' is missing a 'strategy' key")
        elif options["strategy"] not in strategy_map:
            errors.append(
                f"Field '{field}' uses unknown strategy '{options['strategy']}'. "
                f"Available: {list(strategy_map.keys())}"
            )
    return errors