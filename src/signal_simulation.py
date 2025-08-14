import os
import numpy as np
import pandas as pd
from datetime import datetime, UTC
import random

from debugpy.common import timestamp


def simulate_realistic_signal_strength(row, base_dbm=-70.0):
    """
    Signal strength simulation based on ITU-R recommendations and 
    real-world satellite communication principles.
    """
    
    # Extract weather parameters with defaults
    rain_rate = row.get("rain_rate", 0.0) or 0.0
    humidity = row.get("relative_humidity_2m", 50.0) or 50.0
    cloud_cover = row.get("cloudcover", 0.0) or 0.0
    wind_speed = row.get("windspeed_10m", 0.0) or 0.0
    pressure = row.get("pressure_msl", 1013.25) or 1013.25
    temperature = row.get("temperature_2m", 20.0) or 20.0

    # Ensure all are floats, NaNs replaced
    rain_rate = 0.0 if pd.isna(rain_rate) else rain_rate
    humidity = 50.0 if pd.isna(humidity) else humidity
    cloud_cover = 0.0 if pd.isna(cloud_cover) else cloud_cover
    wind_speed = 0.0 if pd.isna(wind_speed) else wind_speed
    pressure = 1013.25 if pd.isna(pressure) else pressure
    temperature = 20.0 if pd.isna(temperature) else temperature

    # Rain attenuation based on ITU-R P.838 model (simplified)
    if rain_rate < 1.0:
        rain_attenuation = rain_rate * 0.2  # Light precipitation
    elif rain_rate < 5.0:
        rain_attenuation = 0.2 + (rain_rate - 1.0) * 0.5  # Moderate precipitation
    else:
        rain_attenuation = 2.2 + (rain_rate - 5.0) * 1.2  # Heavy precipitation
    
    # Water vapor absorption effects
    humidity_normalized = max(0, (humidity - 30) / 70)  # Above 30% threshold
    humidity_attenuation = humidity_normalized ** 2 * 3.0  # Quadratic absorption model
    
    # Cloud scattering effects (varies by cloud density)
    if cloud_cover < 20:
        cloud_attenuation = 0
    elif cloud_cover < 50:
        cloud_attenuation = (cloud_cover - 20) * 0.02  # Thin clouds
    else:
        cloud_attenuation = 0.6 + (cloud_cover - 50) * 0.04  # Dense clouds
    
    # Wind effects on signal path stability
    # Low wind reduces path obstacles, high wind causes signal fluctuation
    if wind_speed < 5:
        wind_effect = -wind_speed * 0.1  # Path clearing benefit
    else:
        wind_effect = (wind_speed - 5) * 0.15  # Signal instability
    
    # Atmospheric density effects from pressure variations
    pressure_deviation = abs(pressure - 1013.25)
    pressure_attenuation = pressure_deviation * 0.01
    
    # Temperature effects on atmospheric refractivity
    temp_effect = abs(temperature - 20) * 0.05
    
    # Coupled effects (combined weather phenomena)
    rain_wind_interaction = rain_rate * wind_speed * 0.02
    humidity_temp_interaction = (humidity / 100) * abs(temperature - 20) * 0.1
    
    # Diurnal atmospheric variations
    hour = timestamp.hour if hasattr(timestamp, 'hour') else 12
    time_effect = np.sin(2 * np.pi * hour / 24) * 1.5  # Daily atmospheric cycle
    
    # Seasonal atmospheric changes
    month = timestamp.month if hasattr(timestamp, 'month') else 6
    seasonal_effect = np.sin(2 * np.pi * month / 12) * 0.8
    
    # Calculate total attenuation
    total_attenuation = (
        rain_attenuation + 
        humidity_attenuation + 
        cloud_attenuation + 
        wind_effect + 
        pressure_attenuation + 
        temp_effect + 
        rain_wind_interaction + 
        humidity_temp_interaction +
        time_effect +
        seasonal_effect
    )
    
    # Base signal calculation
    signal_strength = base_dbm - total_attenuation
    
    # Signal measurement noise from various sources
    # Equipment thermal noise
    equipment_noise = np.random.normal(0, 1.5)
    
    # Atmospheric scintillation (weather-dependent)
    scintillation_factor = 1 + rain_rate * 0.2 + wind_speed * 0.1
    atmospheric_noise = np.random.normal(0, 0.8 * scintillation_factor)
    
    # Intermittent interference sources
    if np.random.random() < 0.05:  # 5% probability
        interference = np.random.uniform(-5, -2)  # Signal degradation event
    else:
        interference = 0
    
    # Multipath propagation effects
    if humidity > 80 and temperature > 25:  # Ducting conditions
        multipath_noise = np.random.normal(0, 2.0)
    else:
        multipath_noise = np.random.normal(0, 0.5)
    
    # Add all noise components
    total_noise = equipment_noise + atmospheric_noise + interference + multipath_noise
    signal_strength += total_noise
    
    # Apply system hardware limitations
    signal_strength = np.clip(signal_strength, -120, -40)  # Receiver dynamic range
    
    # Equipment measurement quantization
    signal_strength = base_dbm if pd.isna(signal_strength) else round(signal_strength * 2) / 2

    
    return signal_strength

def add_missing_data_simulation(df, missing_rate=0.05):
    """
    Simulate sensor failures and data collection issues
    """
    df_copy = df.copy()
    
    # Randomly set some values to NaN
    for column in ['rain_rate', 'relative_humidity_2m', 'windspeed_10m']:
        mask = np.random.random(len(df_copy)) < missing_rate
        df_copy.loc[mask, column] = np.nan
    
    return df_copy

def add_outliers(df, outlier_rate=0.02):
    """
    Add measurement outliers from equipment malfunctions and extreme conditions
    """
    df_copy = df.copy()
    
    n_outliers = int(len(df_copy) * outlier_rate)
    outlier_indices = np.random.choice(len(df_copy), n_outliers, replace=False)
    
    for idx in outlier_indices:
        # Equipment malfunction on single parameter
        param = np.random.choice(['rain_rate', 'relative_humidity_2m', 'windspeed_10m'])
        if param == 'rain_rate':
            df_copy.loc[idx, param] = np.random.uniform(50, 100)  # Storm conditions
        elif param == 'relative_humidity_2m':
            df_copy.loc[idx, param] = np.random.uniform(95, 100)  # Saturated conditions
        else:
            df_copy.loc[idx, param] = np.random.uniform(30, 50)   # High wind conditions
    
    return df_copy

# Updated to match your original function signature exactly
def simulate_from_csv(input_path, output_subdir="data/simulated"):
    """
    Load weather data, simulate REALISTIC signal strength, and save results.
    
    Args:
        input_path: Path to processed weather CSV.
        output_subdir: Subdirectory under project root to save results.
    """
    from src.utils.logger import get_logger
    from src.utils.config_loader import load_project_root
    
    logger = get_logger(__name__)
    project_root = load_project_root()
    
    output_dir = os.path.join(project_root, output_subdir)
    os.makedirs(output_dir, exist_ok=True)

    # Load data
    df = pd.read_csv(input_path)
    
    # Convert timestamp if it exists
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Add realistic complexity
    df = add_missing_data_simulation(df, missing_rate=0.02)  # 2% missing data
    df = add_outliers(df, outlier_rate=0.015)  # 1.5% outliers
    
    # Generate signal strength using advanced simulation
    np.random.seed(42)  # For reproducible results
    df['signal_dbm'] = df.apply(simulate_realistic_signal_strength, axis=1)
    
    # Add geographic/equipment-specific biases
    if 'location' in df.columns:
        location_bias = {
            'seattle': -1.8,    # Urban environment, frequent precipitation
            'miami': 0.3,       # Coastal conditions, atmospheric ducting
            'phoenix': -0.5,    # High temperature equipment effects
            'denver': -2.2,     # High altitude, atmospheric effects
            'london': -1.4      # Urban density, frequent overcast
        }
        for location, bias in location_bias.items():
            mask = df['location'].str.contains(location, case=False, na=False)
            if mask.any():
                df.loc[mask, 'signal_dbm'] += bias + np.random.normal(0, 0.4, mask.sum())

    # Save to the same path as your original
    output_path = os.path.join(output_dir, "signal_latest.csv")
    df.to_csv(output_path, index=False)
    
    logger.info(f"Saved simulated signal data to {output_path}")
    print(f"Simulation results saved to data/simulated/signal_latest.csv")
    
    # Display signal characteristics
    print(f"\n📊 Signal Strength Statistics:")
    print(f"  Mean: {df['signal_dbm'].mean():.2f} dBm")
    print(f"  Std:  {df['signal_dbm'].std():.2f} dBm") 
    print(f"  Min:  {df['signal_dbm'].min():.2f} dBm")
    print(f"  Max:  {df['signal_dbm'].max():.2f} dBm")
    print(f"  Missing values: {df['signal_dbm'].isna().sum()}")
    
    return df

# Keep your original simulate_signal_strength for comparison (rename it)
def simulate_signal_strength_simple(row, base_dbm=-50.0):
    """
    Your original simple simulation (kept for comparison)
    """
    RAIN_FACTOR = 0.8
    HUMIDITY_FACTOR = 0.05
    CLOUD_FACTOR = 0.03
    WIND_FACTOR = 0.1
    PRESSURE_FACTOR = 0.02
    
    attenuation = (
        RAIN_FACTOR * row.get("rain_rate", 0.0) +
        HUMIDITY_FACTOR * row.get("relative_humidity_2m", 0.0) +
        CLOUD_FACTOR * row.get("cloudcover", 0.0) +
        WIND_FACTOR * row.get("windspeed_10m", 0.0) +
        PRESSURE_FACTOR * row.get("pressure_msl", 0.0)
    )
    return round(base_dbm - attenuation, 2)

# Example usage and testing
if __name__ == "__main__":
    print("Testing signal propagation simulation...")
    
    # Test with sample weather conditions
    sample_data = pd.DataFrame({
        'timestamp': pd.date_range('2024-01-01', periods=100, freq='H'),
        'rain_rate': [0, 1, 5, 10, 20] * 20,  # Various precipitation intensities
        'relative_humidity_2m': [30, 50, 70, 85, 95] * 20,  # Various humidity levels
        'cloudcover': [0, 25, 50, 75, 100] * 20,  # Various cloud conditions
        'windspeed_10m': [2, 5, 10, 15, 25] * 20,  # Various wind conditions
        'pressure_msl': [1010, 1013, 1015, 1020, 1025] * 20,
        'temperature_2m': [10, 15, 20, 25, 30] * 20
    })
    
    # Compare basic vs advanced simulation
    sample_data['signal_basic'] = sample_data.apply(simulate_signal_strength_simple, axis=1)
    sample_data['signal_advanced'] = sample_data.apply(simulate_realistic_signal_strength, axis=1)
    
    print("\n Comparison of Simulation Methods:")
    print("Basic simulation statistics:")
    print(f"  Mean: {sample_data['signal_basic'].mean():.2f} dBm")
    print(f"  Std:  {sample_data['signal_basic'].std():.2f} dBm")
    
    print("\nAdvanced simulation statistics:")  
    print(f"  Mean: {sample_data['signal_advanced'].mean():.2f} dBm")
    print(f"  Std:  {sample_data['signal_advanced'].std():.2f} dBm")
    print(f"  Range: {sample_data['signal_advanced'].min():.1f} to {sample_data['signal_advanced'].max():.1f} dBm")