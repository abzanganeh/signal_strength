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
    {"name": "Seattle", "latitude": 47.6062, "longitude": -122.3321},
    {"name": "Chicago", "latitude": 41.8781, "longitude": -87.6298},
    {"name": "Phoenix", "latitude": 33.4484, "longitude": -112.0740},
    {"name": "Miami", "latitude": 25.7617, "longitude": -80.1918},
    {"name": "Denver", "latitude": 39.7392, "longitude": -104.9903},
    {"name": "San Francisco", "latitude": 37.7749, "longitude": -122.4194},
    {"name": "New York", "latitude": 40.7128, "longitude": -74.0060},
    {"name": "London", "latitude": 51.5074, "longitude": -0.1278},
    {"name": "Tokyo", "latitude": 35.6895, "longitude": 139.6917},
    {"name": "Sydney", "latitude": -33.8688, "longitude": 151.2093}
]

# Timezone for API queries
DEFAULT_TIMEZONE = "auto"
