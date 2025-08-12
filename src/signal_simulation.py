import os
import pandas as pd
from datetime import datetime

from src.utils.logger import get_logger
from src.utils.config_loader import load_project_root

logger = get_logger(__name__)
project_root = load_project_root()

# Attenuation coefficients
RAIN_FACTOR = 0.8       # dB per mm/hr
HUMIDITY_FACTOR = 0.05  # dB per % humidity
CLOUD_FACTOR = 0.03     # dB per % cloud cover
WIND_FACTOR = 0.1       # dB per m/s wind speed
BASE_DBM = -50.0        # Reference signal strength

def simulate_signal_strength(row, base_dbm=BASE_DBM):
    """
    Simulate signal strength degradation based on weather features.

    Args:
        row: DataFrame row with weather features.
        base_dbm: Reference signal strength.

    Returns:
        float: Simulated signal strength in dBm.
    """
    attenuation = (
        RAIN_FACTOR * row.get("rain_rate", 0.0) +
        HUMIDITY_FACTOR * row.get("humidity", 0.0) +
        CLOUD_FACTOR * row.get("cloud_cover", 0.0) +
        WIND_FACTOR * row.get("wind_speed", 0.0)
    )
    return round(base_dbm - attenuation, 2)

def simulate_from_csv(input_path, output_subdir="data/simulated"):
    """
    Load weather data, simulate signal strength, and save results.

    Args:
        input_path: Path to processed weather CSV.
        output_subdir: Subdirectory under project root to save results.
    """
    output_dir = os.path.join(project_root, output_subdir)
    os.makedirs(output_dir, exist_ok=True)

    df = pd.read_csv(input_path)
    df["signal_dbm"] = df.apply(simulate_signal_strength, axis=1)

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M")
    output_path = os.path.join(output_dir, f"signal_{timestamp}.csv")
    df.to_csv(output_path, index=False)
    logger.info(f"✅ Saved simulated signal data to {output_path}")

if __name__ == "__main__":
    # Example usage
    input_file = os.path.join(project_root, "data", "processed", "weather_latest.csv")
    simulate_from_csv(input_file)
