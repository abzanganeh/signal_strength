import os
import re


def get_latest_file_by_prefix(directory, prefix):
    files = [f for f in os.listdir(directory) if f.startswith(prefix)]
    if not files:
        raise FileNotFoundError(f"No files found in {directory} with prefix '{prefix}'")
    latest_file = max(files, key=lambda x: os.path.getctime(os.path.join(directory, x)))
    return os.path.join(directory, latest_file)

def get_latest_engineered_file(project_root):
    processed_dir = os.path.join(project_root, "data", "processed")
    return get_latest_file_by_prefix(processed_dir, "weather_engineered_")

def safe_name(location_name):
    return re.sub(r'[^A-Za-z0-9_.-]', '_', location_name)

def validate_simulation_input(df, required_columns):
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns for simulation: {missing}")
    print("Input schema validated.")