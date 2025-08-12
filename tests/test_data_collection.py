import pytest
import pandas as pd
import os
import tempfile

from src.utils.config import OPENWEATHER_API_KEY
from src.utils.constants import DEFAULT_LOCATIONS
from src.data_collection import fetch_weather, parse_weather_json

@pytest.fixture
def sample_location():
    return DEFAULT_LOCATIONS[0]  # Seattle

def test_fetch_weather_keys(sample_location):
    """
    Test that API response contains expected top-level keys.
    """
    assert OPENWEATHER_API_KEY, "Missing OpenWeatherMap API key"
    with tempfile.TemporaryDirectory() as tmpdir:
        data = fetch_weather(
            sample_location["name"],
            sample_location["latitude"],
            sample_location["longitude"],
            save_dir=tmpdir
        )
        assert "main" in data, "'main' section missing in API response"
        assert "wind" in data, "'wind' section missing in API response"
        assert "clouds" in data, "'clouds' section missing in API response"

def test_parse_weather_json_structure(sample_location):
    """
    Test that parsed weather JSON returns expected keys.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        raw_data = fetch_weather(
            sample_location["name"],
            sample_location["latitude"],
            sample_location["longitude"],
            save_dir=tmpdir
        )
        parsed = parse_weather_json(raw_data)
        expected_keys = {
            "timestamp", "temperature", "humidity",
            "pressure", "cloud_cover", "wind_speed", "rain_rate"
        }
        missing = expected_keys - parsed.keys()
        assert not missing, f"Missing keys in parsed data: {missing}"

def test_parse_weather_json_types(sample_location):
    """
    Test that parsed values are of correct types.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        raw_data = fetch_weather(
            sample_location["name"],
            sample_location["latitude"],
            sample_location["longitude"],
            save_dir=tmpdir
        )
        parsed = parse_weather_json(raw_data)

        assert isinstance(parsed["timestamp"], pd.Timestamp), "timestamp should be pd.Timestamp"
        assert isinstance(parsed["temperature"], (int, float)), "temperature should be numeric"
        assert isinstance(parsed["humidity"], int), "humidity should be int"
        assert isinstance(parsed["rain_rate"], float), "rain_rate should be float"
