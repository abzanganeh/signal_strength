import pytest
import pandas as pd
import os
import glob
from src.data_validation import (
    validate_schema,
    check_missing_values,
    check_value_ranges,
    validate_timestamps,
    check_duplicates
)
from src.utils.config_loader import load_project_root


@pytest.fixture(scope="module")
def processed_df():
    project_root = load_project_root()
    processed_dir = os.path.join(project_root, "data", "processed")
    files = sorted(glob.glob(os.path.join(processed_dir, "weather_*.csv")))

    if files:
        print(f"✅ Loaded processed file: {files[-1]}")
        return pd.read_csv(files[-1])
    else:
        print("⚠️ No processed CSV found — using fallback dummy data")
        dummy_data = {
            "timestamp": pd.date_range(start="2025-08-11", periods=5, freq="H"),
            "location": ["Seattle", "Miami", "Phoenix", "Denver", "London"],
            "temperature": [20.5, 30.2, 35.1, 22.0, 18.3],
            "humidity": [60, 70, 20, 50, 80],
            "pressure": [1012, 1010, 1005, 1015, 1013],
            "cloud_cover": [90, 10, 0, 50, 100],
            "wind_speed": [5.2, 3.1, 2.8, 4.0, 6.5],
            "rain_rate": [0.0, 0.2, 0.0, 0.1, 0.3]
        }
        return pd.DataFrame(dummy_data)



# Test 1: Schema validation
def test_schema(processed_df):
    expected_columns = {"timestamp", "location", "temperature", "humidity", "pressure", "cloud_cover", "wind_speed", "rain_rate"}
    missing = validate_schema(processed_df, expected_columns)
    assert missing == set(), f"Missing columns: {missing}"

# Test 2: Missing values
def test_missing_values(processed_df):
    missing = check_missing_values(processed_df)
    assert missing.sum() == 0, f"Found missing values:\n{missing[missing > 0]}"

# Test 3: Value ranges
def test_temperature_range(processed_df):
    outliers = check_value_ranges(processed_df, {"temperature": (-50, 60)})
    assert outliers["temperature"].empty, f"Temperature outliers found:\n{outliers['temperature']}"

# Test 4: Timestamp format
def test_timestamp_validity(processed_df):
    assert validate_timestamps(processed_df), "Invalid timestamp format detected"

# Test 5: Duplicate rows
def test_no_duplicates(processed_df):
    duplicates = check_duplicates(processed_df)
    assert duplicates == 0, f"Found {duplicates} duplicate rows"

def test_humidity_range(processed_df):
    outliers = check_value_ranges(processed_df, {"humidity": (0, 100)})
    assert outliers["humidity"].empty, f"Humidity outliers found:\n{outliers['humidity']}"
