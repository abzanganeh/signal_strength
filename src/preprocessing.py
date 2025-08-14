import os
import pandas as pd
from src.feature_engineering import engineer_features
from src.utils.logger import get_logger
from src.utils.config_loader import load_project_root
from src.utils.utils import safe_name

logger = get_logger(__name__)
project_root = load_project_root()

def handle_null_values(df):
    for col in df.columns[df.isna().any()]:
        if 'location' in df.columns:
            df[col] = df.groupby('location')[col].transform(lambda group: group.ffill().bfill())
        else:
            df[col] = df[col].ffill().bfill()
    return df

def preprocess(df, save=True, preserve_nulls=False):
    if not preserve_nulls:
        df = handle_null_values(df)
    df["location"] = df["location"].apply(safe_name)
    df = handle_null_values(df)
    df = engineer_features(df)

    if save:
        output_path = os.path.join(project_root, "data", "processed", "weather_engineered_latest.csv")
        df.to_csv(output_path, index=False)
        logger.info(f"✅ Saved engineered features to {output_path}")

    return df
