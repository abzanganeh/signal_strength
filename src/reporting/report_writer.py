import os
import pandas as pd
from datetime import datetime, UTC

def generate_markdown_report(model_name, metrics, plot_paths, project_root):
    report_dir = os.path.join(project_root, "results", "reports")
    os.makedirs(report_dir, exist_ok=True)

    timestamp = datetime.now(UTC).strftime("%Y-%m-%d_%H-%M-%S")
    report_filename = f"{model_name}_report_{timestamp}.md"
    report_path = os.path.join(report_dir, report_filename)

    with open(report_path, "w") as f:
        f.write(f"# {model_name.upper()} Model Report\n\n")
        f.write(f"**Timestamp:** {timestamp}\n\n")
        f.write("## Metrics\n")
        for k, v in metrics.items():
            f.write(f"- {k}: {v:.2f}\n")
        f.write("\n## Plots\n")
        for label, path in plot_paths.items():
            rel_path = os.path.relpath(path, project_root)
            f.write(f"![{label}]({rel_path})\n")

    # Log to report manifest
    manifest_path = os.path.join(report_dir, "report_manifest.csv")
    log_entry = {
        "timestamp": timestamp,
        "model": model_name,
        "report_file": report_filename,
        **{k.lower(): round(v, 2) for k, v in metrics.items()}
    }
    df_log = pd.DataFrame([log_entry])
    df_log.to_csv(manifest_path, mode="a" if os.path.exists(manifest_path) else "w",
                  header=not os.path.exists(manifest_path), index=False)

    return report_path
