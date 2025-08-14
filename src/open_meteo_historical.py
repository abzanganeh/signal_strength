import os
import requests
import pandas as pd
from datetime import datetime
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from src.utils.config import START_DATE, END_DATE
from src.utils.logger import get_logger
from src.utils.constants import DEFAULT_LOCATIONS, EXPECTED_COLUMNS, DEFAULT_TIMEZONE, BASE_URL_HISTORICAL
from src.utils.config_loader import load_project_root

logger = get_logger(__name__)
project_root = load_project_root()
OUTPUT_DIR = os.path.join(project_root, "data", "processed")

def fetch_open_meteo(city, lat, lon):
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": START_DATE,
        "end_date": END_DATE,
        "hourly": EXPECTED_COLUMNS[:-2],  # exclude 'location' and 'time'
        "timezone": DEFAULT_TIMEZONE
    }

    session = requests.Session()
    retries = Retry(total=3, backoff_factor=1, status_forcelist=[502, 503, 504])
    session.mount("https://", HTTPAdapter(max_retries=retries))

    try:
        response = session.get(BASE_URL_HISTORICAL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data["hourly"])
        df["location"] = city
        return df
    except requests.exceptions.RequestException as e:
        logger.warning(f"Failed to fetch data for {city}: {e}")
        return None

def collect_all():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    all_dfs = []

    for loc in DEFAULT_LOCATIONS:
        city = loc["name"]
        lat = loc["latitude"]
        lon = loc["longitude"]
        df = fetch_open_meteo(city, lat, lon)
        if df is not None:
            all_dfs.append(df)
        else:
            logger.warning(f"Skipping {city} due to fetch failure.")

    if all_dfs:
        full_df = pd.concat(all_dfs, ignore_index=True)
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M")
        output_path = os.path.join(OUTPUT_DIR, f"weather_historical_{timestamp}.csv")
        full_df.to_csv(output_path, index=False)
        logger.info(f"Saved historical weather data to {output_path}")
    else:
        logger.error("No data collected. All fetches failed.")
