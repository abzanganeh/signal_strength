# src/evaluation.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np
from src.models import get_model
from src.preprocessing import preprocess


def evaluate(df, model_name, target_column="signal_dbm"):
    # Decide whether to preserve nulls
    preserve_nulls = model_name in ["xgb", "stack"]

    # Run full preprocessing pipeline
    df = preprocess(df, save=False, preserve_nulls=preserve_nulls)

    # Drop non-feature columns
    X = df.select_dtypes(include=["number"]).copy()
    y = df[target_column]

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Get and train model
    model = get_model(model_name)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # Evaluate
    metrics = {
        "MAE": mean_absolute_error(y_test, y_pred),
        "RMSE": np.sqrt(mean_squared_error(y_test, y_pred)),
        "R2": r2_score(y_test, y_pred)
    }

    return metrics, y_test, y_pred
