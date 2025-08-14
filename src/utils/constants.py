# Weather API base URL
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
BASE_URL_HISTORICAL = "https://archive-api.open-meteo.com/v1/archive"

# Expected schema for weather data
EXPECTED_COLUMNS = [
    "temperature_2m", "relative_humidity_2m", "pressure_msl",
    "cloudcover", "windspeed_10m", "rain", "location", "time"
]

# Valid ranges for each feature
RANGE_CHECKS = {
    "temperature_2m": (-50, 50),
    "relative_humidity_2m": (0, 100),
    "pressure_msl": (900, 1100),
    "cloudcover": (0, 100),
    "windspeed_10m": (0, 150),
    "rain": (0, 100)
}

# Default locations for data collection
DEFAULT_LOCATIONS = [
    # Original US Cities
    {"name": "Seattle", "latitude": 47.6062, "longitude": -122.3321},
    {"name": "Chicago", "latitude": 41.8781, "longitude": -87.6298},
    {"name": "Phoenix", "latitude": 33.4484, "longitude": -112.0740},
    {"name": "Miami", "latitude": 25.7617, "longitude": -80.1918},
    {"name": "Denver", "latitude": 39.7392, "longitude": -104.9903},
    {"name": "San Francisco", "latitude": 37.7749, "longitude": -122.4194},
    {"name": "New York", "latitude": 40.7128, "longitude": -74.0060},
    # Global Cities
    {"name": "London", "latitude": 51.5074, "longitude": -0.1278},
    {"name": "Tokyo", "latitude": 35.6895, "longitude": 139.6917},
    {"name": "Sydney", "latitude": -33.8688, "longitude": 151.2093},
    {"name": "Mumbai", "latitude": 19.0760, "longitude": 72.8777},         # Monsoon-heavy
    {"name": "Singapore", "latitude": 1.3521, "longitude": 103.8198},      # Equatorial rain
    {"name": "Bangkok", "latitude": 13.7563, "longitude": 100.5018},       # Tropical wet/dry
    {"name": "Kuala Lumpur", "latitude": 3.1390, "longitude": 101.6869},   # Humid tropical
    {"name": "Cape Town", "latitude": -33.9249, "longitude": 18.4241},     # Mediterranean
    {"name": "São Paulo", "latitude": -23.5505, "longitude": -46.6333},    # Subtropical
    {"name": "Cairo", "latitude": 30.0444, "longitude": 31.2357},          # Arid desert
    {"name": "Moscow", "latitude": 55.7558, "longitude": 37.6173},         # Continental
    {"name": "Reykjavik", "latitude": 64.1265, "longitude": -21.8174},     # Subpolar oceanic
    {"name": "Nairobi", "latitude": -1.2921, "longitude": 36.8219}         # Equatorial highland
]
# Timezone for API queries
DEFAULT_TIMEZONE = "auto"
