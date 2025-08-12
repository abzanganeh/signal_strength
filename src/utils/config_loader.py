from pathlib import Path
import yaml

def load_project_root():
    config_path = Path(__file__).resolve().parents[2] / "config.yaml"

    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found at: {config_path}")

    try:
        with config_path.open("r") as f:
            config = yaml.safe_load(f)
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Error parsing YAML file: {e}")

    try:
        return config["paths"]["project_root"]
    except KeyError as e:
        raise KeyError(f"Missing key in config.yaml: {e}")
