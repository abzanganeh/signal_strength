from typing import dataclass_transform

import requests
import json
import os
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime

from nbclient.client import timestamp

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

# We’ll collect data from 5 cities with diverse weather:
LOCATIONS = {
    "Seattle": {"lat": 47.6062, "lon": -122.3321},
    "Miami": {"lat": 25.7617, "lon": -80.1918},
    "Phoenix": {"lat": 33.4484, "lon": -112.0740},
    "Denver": {"lat": 39.7392, "lon": -104.9903},
    "London": {"lat": 51.5074, "lon": -0.1278}
}

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def fetch_weather(location_name, lat, lon):
    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "metric"
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    #save raw json
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M")
    raw_path = f"data/raw/{location_name}_{timestamp}.json"
    with open(raw_path, "w") as f:
        json.dump(data, f, indent=2)
    return data

def parse_weather_json(data):
    parsed = {
        "timestamp": datetime.utcnow(),
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "pressure": data["main"]["pressure"],
        "cloud_cover": data["clouds"]["all"],
        "wind_speed": data["wind"]["speed"],
        "rain_rate": data.get("rain", {}).get("1h", 0.0)  # default to 0 if no rain
    }
    return parsed


def collect_all_locations():
    records = []
    for name, coords in LOCATIONS.items():
        raw_data = fetch_weather(name, coords["lat"], coords["lon"])
        parsed = parse_weather_json(raw_data)
        parsed["location"] = name
        records.append(parsed)

    df = pd.DataFrame(records)
    processed_path = f"data/processed/weather_{datetime.utcnow().strftime('%Y%m%d_%H%M')}.csv"
    df.to_csv(processed_path, index=False)
    print(f"Saved processed data to {processed_path}")

