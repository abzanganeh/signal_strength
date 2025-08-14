import os
from datetime import datetime, UTC

import pandas as pd
from src.utils import utils
from src.utils.config_loader import load_project_root
from src.open_meteo_historical import collect_all
from src.utils.utils import get_latest_engineered_file, validate_simulation_input
from src.preprocessing import preprocess
from src.signal_simulation import simulate_from_csv
import argparse
import re


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, help="Path to engineered weather file")
    parser.add_argument("--refresh", action="store_true", help="Force refresh of historical weather data")
    return parser.parse_args()

def get_latest_historical_file(project_root):
    processed_dir = os.path.join(project_root, "data", "processed")
    files = [f for f in os.listdir(processed_dir) if f.startswith("weather_historical_")]
    if not files:
        raise FileNotFoundError(f"No historical weather files found in {processed_dir}")
    latest_file = max(files, key=lambda x: os.path.getctime(os.path.join(processed_dir, x)))
    return os.path.join("data", "processed", latest_file)

def main():
    project_root = load_project_root()

    # Ensure historical data is available
    processed_dir = os.path.join(project_root, "data", "processed")
    historical_files = [f for f in os.listdir(processed_dir) if f.startswith("weather_historical_")]
    args = parse_args()
    if args.refresh or not historical_files:
        print("📡 Collecting historical weather data...")
        collect_all()

    #Now safely get the latest file
    latest_file = get_latest_historical_file(project_root)

    df_featured = preprocess(latest_file)
    print(f"Loaded historical data from {latest_file}")
    match = re.search(r"weather_historical_(\d{8}_\d{4})\.csv", latest_file)
    if match:
        print(f"🕒 Data timestamp: {match.group(1)}")
    print(df_featured.head())

    input_file = args.input if args.input else get_latest_engineered_file(project_root)
    simulate_from_csv(input_file)
    log_entry = {
        "timestamp": datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S"),
        "engineered_file": "weather_engineered_latest.csv",
        "signal_file": "signal_latest.csv"
    }

    manifest_path = os.path.join(project_root, "run_log.csv")
    df_log = pd.DataFrame([log_entry])

    if os.path.exists(manifest_path):
        df_log.to_csv(manifest_path, mode="a", header=False, index=False)
    else:
        df_log.to_csv(manifest_path, index=False)

    print(f"📜 Logged run to {manifest_path}")

if __name__ == "__main__":
    main()
