import pandas as pd
import numpy as np

from src.utils.logger import get_logger
from src.utils.constants import EXPECTED_COLUMNS, RANGE_CHECKS

logger = get_logger(__name__)

def validate_schema(df, expected_columns=EXPECTED_COLUMNS):
    """
    Checks if all expected columns are present in the DataFrame.

    Args:
        df: Input DataFrame.
        expected_columns: List of required column names.

    Returns:
        set: Missing columns, if any.
    """
    missing = set(expected_columns) - set(df.columns)
    if missing:
        logger.warning(f"Missing columns: {missing}")
    else:
        logger.info("Schema validation passed.")
    return missing

def check_missing_values(df):
    """
    Checks for missing values in each column.

    Args:
        df: Input DataFrame.

    Returns:
        pd.Series: Count of missing values per column.
    """
    missing = df.isnull().sum()
    if missing.sum() > 0:
        logger.warning(f"Missing values detected:\n{missing}")
    else:
        logger.info("No missing values found.")
    return missing

def check_value_ranges(df, range_checks=RANGE_CHECKS):
    """
    Checks for out-of-range values based on predefined limits.

    Args:
        df: Input DataFrame.
        range_checks: Dict of column → (min, max) range.

    Returns:
        dict: Column → DataFrame of outliers.
    """
    outliers = {}
    for col, (min_val, max_val) in range_checks.items():
        if col in df.columns:
            mask = (df[col] < min_val) | (df[col] > max_val)
            outliers[col] = df[mask]
            if not outliers[col].empty:
                logger.warning(f"Outliers found in '{col}': {len(outliers[col])} rows")
    return outliers

def validate_timestamps(df, column='timestamp'):
    """
    Validates timestamp format in the specified column.

    Args:
        df: Input DataFrame.
        column: Column name containing timestamps.

    Returns:
        bool: True if valid, False otherwise.
    """
    try:
        pd.to_datetime(df[column])
        logger.info("Timestamp validation passed.")
        return True
    except Exception as e:
        logger.error(f"Timestamp validation failed: {e}")
        return False

def check_duplicates(df):
    """
    Checks for duplicate rows in the DataFrame.

    Args:
        df: Input DataFrame.

    Returns:
        int: Number of duplicate rows.
    """
    dup_count = df.duplicated().sum()
    if dup_count > 0:
        logger.warning(f"Found {dup_count} duplicate rows.")
    else:
        logger.info("No duplicates found.")
    return dup_count
