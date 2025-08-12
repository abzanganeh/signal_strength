import os
import pandas as pd
from datetime import datetime
from src.utils.logger import get_logger
from src.utils.config_loader import load_project_root
from src.feature_engineering import engineer_features


logger = get_logger(__name__)
project_root = load_project_root()

def preprocess(file_path):
    full_path = os.path.join(project_root, file_path)
    df = pd.read_csv(full_path)
    df_features = engineer_features(df)

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M")
    output_path = os.path.join(project_root, "data", "processed", f"weather_engineered_{timestamp}.csv")
    df_features.to_csv(output_path, index=False)
    logger.info(f"Saved engineered features to {output_path}")
    return df_features

