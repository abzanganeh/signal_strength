import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def plot_predictions(y_true, y_pred, model_name, project_root):
    output_dir = os.path.join(project_root, "results", "figures")
    os.makedirs(output_dir, exist_ok=True)

    plt.figure(figsize=(6, 6))
    sns.scatterplot(x=y_true, y=y_pred, alpha=0.6)
    plt.plot([min(y_true), max(y_true)], [min(y_true), max(y_true)], color='red', linestyle='--')
    plt.xlabel("Actual")
    plt.ylabel("Predicted")
    plt.title(f"{model_name.upper()} Predictions")
    path = os.path.join(output_dir, f"{model_name}_predictions.png")
    plt.savefig(path)
    plt.close()
    return path

def plot_residuals(y_true, y_pred, model_name, project_root):
    output_dir = os.path.join(project_root, "results", "figures")
    os.makedirs(output_dir, exist_ok=True)

    residuals = np.array(y_true) - np.array(y_pred)
    plt.figure(figsize=(6, 4))
    sns.histplot(residuals, bins=30, kde=True)
    plt.xlabel("Residual")
    plt.title(f"{model_name.upper()} Residuals")
    path = os.path.join(output_dir, f"{model_name}_residuals.png")
    plt.savefig(path)
    plt.close()
    return path

def plot_feature_importance(model, model_name, feature_names, project_root):
    if not hasattr(model, "feature_importances_"):
        return None

    output_dir = os.path.join(project_root, "results", "figures")
    os.makedirs(output_dir, exist_ok=True)

    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1]
    sorted_features = [feature_names[i] for i in indices]

    plt.figure(figsize=(8, 6))
    sns.barplot(x=importances[indices], y=sorted_features)
    plt.title(f"{model_name.upper()} Feature Importance")
    plt.xlabel("Importance")
    path = os.path.join(output_dir, f"{model_name}_feature_importance.png")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
    return path
