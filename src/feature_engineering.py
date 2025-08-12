import pandas as pd

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply feature transformations to raw weather data.
    Returns a DataFrame with engineered features.
    """
    df = df.copy()
    required = ["temperature_2m", "relative_humidity_2m", "windspeed_10m", "time", "location"]
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    # Convert timestamp
    df["time"] = pd.to_datetime(df["time"])

    # Example features
    df["temp_celsius"] = df["temperature_2m"] - 273.15  # if in Kelvin
    df["humidity_ratio"] = df["relative_humidity_2m"] / 100
    df["wind_power"] = df["windspeed_10m"] ** 2

    # Time-based features
    df["hour"] = df["time"].dt.hour
    df["day_of_week"] = df["time"].dt.dayofweek

    # Normalize location names
    df["location"] = df["location"].str.lower()

    return df
