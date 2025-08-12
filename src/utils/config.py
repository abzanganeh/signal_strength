import os
from dotenv import load_dotenv

# Load environment variables from .env file at project root
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))
load_dotenv(dotenv_path=env_path)

# Access specific variables
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

if OPENWEATHER_API_KEY is None:
    raise ValueError("Missing OPENWEATHER_API_KEY in .env file")

# Time range for historical data
START_DATE = "2023-01-01"
END_DATE = "2023-12-31"

# Data collection options
USE_CACHE = True
SAVE_RAW_DATA = True
