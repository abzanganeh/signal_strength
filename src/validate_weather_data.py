import os
import pandas as pd

from src.utils.logger import get_logger
from src.utils.constants import EXPECTED_COLUMNS, RANGE_CHECKS
from src.utils.config_loader import load_project_root
from src.data_validation import (
    validate_schema,
    check_missing_values,
    check_value_ranges,
    validate_timestamps,
    check_duplicates
)

logger = get_logger(__name__)
project_root = load_project_root()

def validate_weather_data(file_path):
    """
    Validates weather data from a CSV file.

    Args:
        file_path: Relative path to the CSV file from project root.

    Returns:
        pd.DataFrame: Cleaned DataFrame with valid rows.
    """
    full_path = os.path.join(project_root, file_path)
    logger.info(f"Loading data from {full_path}")
    df = pd.read_csv(full_path)

    # Step 1: Validate schema
    missing_cols = validate_schema(df)
    if missing_cols:
        raise ValueError(f"Missing columns: {missing_cols}")
    logger.info("Schema check passed.")

    # Step 2: Validate timestamp format
    if not validate_timestamps(df, column="time"):
        raise ValueError("Invalid timestamp format in 'time' column.")

    # Step 3: Check for missing values
    missing = check_missing_values(df)

    # Step 4: Check for out-of-range values
    outliers = check_value_ranges(df)

    # Step 5: Check for duplicate rows
    dup_count = check_duplicates(df)

    # Step 6: Drop rows with missing values
    df_clean = df.dropna()
    logger.info(f"Cleaned data: {len(df_clean)} rows remaining after dropping missing values.")

    return df_clean
