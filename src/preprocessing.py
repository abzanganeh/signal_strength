import os
import pandas as pd
from datetime import datetime
from src.feature_engineering import engineer_features
from src.utils.logger import get_logger
from src.utils.config_loader import load_project_root
from src.utils.utils import safe_name  # assuming this exists


logger = get_logger(__name__)
project_root = load_project_root()


def handle_null_values(df):
    missing_summary = df.isna().sum()
    cols_with_null = missing_summary[missing_summary > 0]

    for col in cols_with_null.index:
        if 'location' in df.columns:
            df[col] = df.groupby('location')[col].transform(lambda group: group.ffill().bfill())
        else:
            df[col] = df[col].ffill().bfill()
    return df

def preprocess(file_path, save=True):
    full_path = os.path.join(project_root, file_path)
    df = pd.read_csv(full_path)
    df["location"] = df["location"].apply(safe_name)
    df = handle_null_values(df)
    df_features = engineer_features(df)

    if save:
        output_path = os.path.join(project_root, "data", "processed", "weather_engineered_latest.csv")
        df_features.to_csv(output_path, index=False)
        logger.info(f"✅ Overwrote engineered features at {output_path}")

    return df_features
