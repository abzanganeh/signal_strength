# 📡 Satellite Signal Strength Prediction  
### A Supervised Regression Pipeline for Estimating Signal Quality from Weather Conditions

---

## Overview

This project builds regression models to predict **satellite signal strength (in dBm)** using weather and atmospheric data. It follows a structured, reproducible workflow:

- **Simple Linear Regression** – using rain rate as a predictor  
- **Multiple Regression** – incorporating temperature, humidity, pressure, etc.  
- **Non-linear Models** – Random Forest, XGBoost  
- **Advanced Optimization** – feature engineering, hyperparameter tuning, SHAP analysis

---

## Business Relevance

Accurate signal prediction helps satellite internet providers:

- Maintain service quality during adverse weather  
- Proactively notify customers of potential disruptions  
- Optimize transmission power and resource allocation  
- Reduce downtime and improve customer satisfaction

---

## Technical Goals

- Collect real-time and historical weather data from public APIs  
- Simulate signal degradation using physics-inspired models  
- Build and evaluate regression algorithms with interpretable outputs  
- Identify key weather factors affecting signal strength  
- Create a reproducible, testable, and maintainable pipeline

---

## Tech Stack

- **Languages & Libraries**: `Python`, `pandas`, `numpy`, `scikit-learn`, `matplotlib`, `seaborn`, `xgboost`, `shap`, `requests`  
- **APIs**: `OpenWeatherMap` (free tier)  
- **Tools**: `Jupyter Notebook`, `PyCharm`, `Git`, `pytest`, `dotenv`, `yaml`  

---

## Location Coverage

Weather data is collected from diverse global locations to ensure model generalization:

- Seattle 🇺🇸  
- Chicago 🇺🇸  
- Phoenix 🇺🇸  
- Miami 🇺🇸  
- Denver 🇺🇸  
- San Francisco 🇺🇸  
- New York 🇺🇸  
- London 🇬🇧  
- Tokyo 🇯🇵  
- Sydney 🇦🇺  

---

## Project Structure
```
Satellite-Signal-Prediction/
│  ├── data/ 
│  ├── raw/ # Unprocessed weather data from API 
│  ├── processed/ # Cleaned and feature-engineered datasets 
│  └── simulated/ # Datasets with simulated signal strength  
│
├── notebooks/ 
│  ├── 01_exploration.ipynb #Initial data exploration 
│  ├── 02_modeling_baseline.ipynb # Linear regression 
│  └── 03_modeling_advanced.ipynb # Non-linear models and tuning 
│ 
├── results/
│  ├── figures/ # Plots and visualizations 
│  ├── models/ # Saved model files
│  └── reports/ # Summary reports and metrics 
│
├── src/ 
│   ├── data_collection.py # Weather API scripts 
│   ├── data_validation.py # Schema and quality checks 
│   ├── signal_simulation.py # Signal strength simulation logic
│   ├── preprocessing.py # Data cleaning and feature engineering
│   ├── modeling.py # Model training and evaluation
│   ├── open_meteo_historical.py # Gather Historical data
│   ├── validate_weather_data.py # Historical data validation 
│   └── utils/ 
│       ├── logger.py 
│       ├── config_loader.py
│       ├── constants.py
│       └── helpers.py
│ 
├── tests/
│  ├── test_data_collection.py # Unit tests for data collection
│  └── test_data_validation.py # Unit tests for validation logic
│  
├── .env # Environment variables (e.g. API keys)
├── config.yaml # Optional config file for project root
├── .gitignore # Git exclusions
├── LICENSE # Project license
├── main.py # Entry point (optional)
├── README.md # Project documentation
├── project.llm
└── requirements.txt # Python dependencies
```

---

## Testing Setup

To run tests locally or in CI:

### Option 1: Use Environment Variable

```
export PROJECT_ROOT=/Users/admin/Desktop/projects/signal_strength
```
### Option 2: Use `config.yaml`:
```
paths:
  project_root: /Users/admin/Desktop/projects/signal_strength
```
The test fixture processed_df will automatically load the latest processed weather data from data/processed/, or fall back to dummy data if none is found.

## Modeling Philosophy
This project avoids opaque automation and AI shortcuts. Every step is:

- Transparent and interpretable

- Executed manually or with traceable logic

- Designed for reproducibility and auditability

- Focused on real-world business relevance

## Author
Alireza Barzin Zanganeh 
Machine Learning Engineer | Backend & QA Automation
Committed to structure, transparency, and continuous improvement.

## License
MIT License. See LICENSE for details.