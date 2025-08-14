import pandas as pd
from src.utils.config import DROP_COLUMNS

def engineer_features(df: pd.DataFrame, verbose: bool = False) -> pd.DataFrame:
    df = df.copy()

    # Convert timestamp
    df["time"] = pd.to_datetime(df["time"], errors="coerce")

    # Basic features
    df["temperature_celsius"] = df.get("temperature_2m", df.get("temperature_celsius"))
    df["humidity_ratio"] = df["relative_humidity_2m"] / 100
    df["wind_power"] = df["windspeed_10m"] ** 2

    # Time features
    df["hour"] = df["time"].dt.hour
    df["day"] = df["time"].dt.day
    df["month"] = df["time"].dt.month
    df["weekday"] = df["time"].dt.weekday

    # Normalize location
    df["location"] = df["location"].str.lower()

    # Composite key
    df["time_location"] = df["time"].astype(str) + "_" + df["location"]
    df.set_index("time_location", inplace=True)

    # Drop intermediate columns
    df.drop(columns=["temperature_2m"] + DROP_COLUMNS, inplace=True, errors='ignore')

    # Preserve target column
    if "signal_dbm" not in df.columns:
        raise ValueError("Target column 'signal_dbm' missing after feature engineering.")

    if verbose:
        print("Final columns:", df.columns.tolist())

    return df
