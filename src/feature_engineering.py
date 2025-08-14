import pandas as pd
from src.utils.config import REQUIRED_FOR_SIMULATION, DROP_COLUMNS


def engineer_features(df: pd.DataFrame, verbose: bool = False) -> pd.DataFrame:
    df = df.copy()

    # Convert timestamp
    df["time"] = pd.to_datetime(df["time"], errors="coerce")

    # Basic feature engineering
    df["temperature_celsius"] = df["temperature_2m"]
    df["humidity_ratio"] = df["relative_humidity_2m"] / 100
    df["wind_power"] = df["windspeed_10m"] ** 2

    # Time-based features
    df["hour"] = df["time"].dt.hour
    df["day"] = df["time"].dt.day
    df["month"] = df["time"].dt.month
    df["weekday"] = df["time"].dt.weekday

    # Normalize location
    df["location"] = df["location"].str.lower()

    # Composite key
    df["time_location"] = df["time"].astype(str) + "_" + df["location"]
    df.set_index("time_location", inplace=True)

    # Rename for clarity
    df.rename(columns={"rain": "rain_rate"}, inplace=True)

    # Drop intermediate columns
    df.drop(columns=["temperature_2m"] + DROP_COLUMNS, inplace=True, errors='ignore')

    # ✅ Now validate required columns
    missing = [col for col in REQUIRED_FOR_SIMULATION if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    # Optional diagnostics
    if verbose:
        nat_count = df["time"].isna().sum()
        duplicate_count = df["time"].duplicated().sum()
        location_per_time = df.groupby("time")["location"].nunique()
        multi_location_times = (location_per_time > 1).sum()

        print(f"🕒 NaT timestamps: {nat_count}")
        print(f"🔁 Duplicate timestamps: {duplicate_count}")
        print(f"🌍 Timestamps with multiple locations: {multi_location_times}")

    return df
