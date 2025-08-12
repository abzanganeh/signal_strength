import os
import requests
import pandas as pd
from datetime import datetime

from src.utils.logger import get_logger
from src.utils.constants import DEFAULT_LOCATIONS, EXPECTED_COLUMNS, DEFAULT_TIMEZONE
from src.utils.config_loader import load_project_root

logger = get_logger(__name__)
project_root = load_project_root()

BASE_URL = "https://archive-api.open-meteo.com/v1/archive"
START_DATE = "2024-07-01"
END_DATE = "2024-07-31"
OUTPUT_DIR = os.path.join(project_root, "data", "processed")

def fetch_open_meteo(city, lat, lon):
    """
    Fetch historical weather data from Open-Meteo API.

    Args:
        city: City name.
        lat: Latitude.
        lon: Longitude.

    Returns:
        pd.DataFrame: Hourly weather data.
    """
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": START_DATE,
        "end_date": END_DATE,
        "hourly": EXPECTED_COLUMNS[:-2],  # exclude 'location' and 'time'
        "timezone": DEFAULT_TIMEZONE
    }
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    data = response.json()
    df = pd.DataFrame(data["hourly"])
    df["location"] = city
    return df

def collect_all():
    """
    Collect historical weather data for all default locations.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    all_dfs = []
    for loc in DEFAULT_LOCATIONS:
        city = loc["name"]
        lat = loc["latitude"]
        lon = loc["longitude"]
        df = fetch_open_meteo(city, lat, lon)
        all_dfs.append(df)

    full_df = pd.concat(all_dfs, ignore_index=True)
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M")
    output_path = os.path.join(OUTPUT_DIR, f"weather_historical_{timestamp}.csv")
    full_df.to_csv(output_path, index=False)
    logger.info(f"Saved historical weather data to {output_path}")
