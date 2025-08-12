import os
import re
import json
import time
import requests
import pandas as pd
from datetime import datetime

from src.utils.logger import get_logger
from src.utils.config import OPENWEATHER_API_KEY
from src.utils.constants import BASE_URL, DEFAULT_LOCATIONS
from src.utils.config_loader import load_project_root

logger = get_logger(__name__)
project_root = load_project_root()

def fetch_weather(location_name, lat, lon, save_dir="data/raw", retries=3, backoff=2):
    """
    Fetches weather data from OpenWeatherMap API and saves raw JSON.

    Args:
        location_name: Name of the location.
        lat: Latitude.
        lon: Longitude.
        save_dir: Directory to save raw JSON.
        retries: Number of retry attempts.
        backoff: Exponential backoff factor.

    Returns:
        dict: Parsed JSON response.
    """
    save_dir = os.path.join(project_root, save_dir)
    os.makedirs(save_dir, exist_ok=True)

    params = {
        "lat": lat,
        "lon": lon,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }

    safe_name = re.sub(r'[^A-Za-z0-9_.-]', '_', location_name)
    attempt = 0

    while attempt < retries:
        try:
            response = requests.get(BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M")
            raw_path = os.path.join(save_dir, f"{safe_name}_{timestamp}.json")
            with open(raw_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            return data

        except requests.exceptions.RequestException as e:
            logger.warning(f"Attempt {attempt + 1} failed for {location_name}: {e}")
            time.sleep(backoff ** attempt)
            attempt += 1

    raise Exception(f"Failed to fetch weather data for {location_name} after {retries} retries.")

def parse_weather_json(data):
    """
    Parses relevant fields from raw weather JSON.

    Args:
        data: Raw JSON from API.

    Returns:
        dict: Extracted weather metrics.
    """
    timestamp = pd.Timestamp(datetime.utcnow())
    temperature = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    pressure = data["main"]["pressure"]
    cloud_cover = data["clouds"]["all"]
    wind_speed = data["wind"]["speed"]
    rain_rate = data.get("rain", {}).get("1h", 0.0)

    return {
        "timestamp": timestamp,
        "temperature": temperature,
        "humidity": humidity,
        "pressure": pressure,
        "cloud_cover": cloud_cover,
        "wind_speed": wind_speed,
        "rain_rate": rain_rate
    }

def collect_all_locations():
    """
    Collects weather data for all default locations and saves processed CSV.
    """
    records = []
    for loc in DEFAULT_LOCATIONS:
        name = loc["name"]
        lat = loc["latitude"]
        lon = loc["longitude"]
        raw_data = fetch_weather(name, lat, lon)
        parsed = parse_weather_json(raw_data)
        parsed["location"] = name
        records.append(parsed)

    df = pd.DataFrame(records)
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M")
    processed_dir = os.path.join(project_root, "data", "processed")
    os.makedirs(processed_dir, exist_ok=True)
    processed_path = os.path.join(processed_dir, f"weather_{timestamp}.csv")
    df.to_csv(processed_path, index=False)
    logger.info(f"Saved processed data to {processed_path}")
