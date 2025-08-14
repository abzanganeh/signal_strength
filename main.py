import os
import argparse
import pandas as pd
from datetime import datetime, UTC

from src.utils.config_loader import load_project_root
from src.utils.utils import get_latest_historical_file
from src.open_meteo_historical import collect_all
from src.signal_simulation import simulate_from_csv
from src.preprocessing import preprocess
from src.evaluation import evaluate
from src.reporting.plots import plot_predictions, plot_residuals, plot_feature_importance
from src.reporting.report_writer import generate_markdown_report
from src.models import get_model

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--refresh", action="store_true", help="Force refresh of historical weather data")
    return parser.parse_args()

def main():
    project_root = load_project_root()
    args = parse_args()

    # Step 1: Collect historical weather data
    processed_dir = os.path.join(project_root, "data", "processed")
    historical_files = [f for f in os.listdir(processed_dir) if f.startswith("weather_historical_")]
    if args.refresh or not historical_files:
        collect_all()

    historical_path = get_latest_historical_file(project_root)

    # Step 2: Simulate signal from historical weather
    df, signal_path = simulate_from_csv(historical_path)

    # Step 3: Preprocess and engineer features
    # df = preprocess(signal_path, save=True)

    # Step 4: Evaluate models
    model_list = ["lr", "rf", "xgb", "poly", "stack"]
    manifest_path = os.path.join(project_root, "run_log.csv")

    for model_name in model_list:
        print(f"\nEvaluating model: {model_name.upper()}")
        metrics, y_true, y_pred = evaluate(df.copy(), model_name)

        print("Performance:")
        for k, v in metrics.items():
            print(f"{k}: {v:.2f}")

        # Log run
        log_entry = {
            "timestamp": datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S"),
            "weather_file": os.path.basename(historical_path),
            "signal_file": os.path.basename(signal_path),
            "model": model_name,
            **{k.lower(): round(v, 2) for k, v in metrics.items()}
        }
        df_log = pd.DataFrame([log_entry])
        df_log.to_csv(manifest_path, mode="a" if os.path.exists(manifest_path) else "w",
                      header=not os.path.exists(manifest_path), index=False)

        # Generate plots
        plot_paths = {
            "Predictions": plot_predictions(y_true, y_pred, model_name, project_root),
            "Residuals": plot_residuals(y_true, y_pred, model_name, project_root)
        }

        # Feature importance
        if model_name in ["rf", "xgb"]:
            model = get_model(model_name)
            feature_names = df.drop(columns=["signal_dbm", "location", "timestamp"], errors="ignore").columns.tolist()
            importance_path = plot_feature_importance(model, model_name, feature_names, project_root)
            if importance_path:
                plot_paths["Feature Importance"] = importance_path

        # Generate report
        report_path = generate_markdown_report(model_name, metrics, plot_paths, project_root)
        print(f"Report saved to: {report_path}")

if __name__ == "__main__":
    main()
