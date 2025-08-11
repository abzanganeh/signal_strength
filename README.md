# 📡 Satellite Signal Strength Prediction  
### A Supervised Regression Project for Predicting Signal Quality Based on Weather Conditions

---

##  Overview

This project develops machine learning models to predict **satellite signal strength (in dBm)** based on weather conditions and atmospheric factors. It follows a structured learning path:

- **Simple Linear Regression** – using one feature (rain rate)
- **Multiple Regression** – incorporating multiple weather features
- **Non-linear Models** – Random Forest, XGBoost
- **Advanced Optimization** – feature engineering, hyperparameter tuning

###  Business Relevance

Accurate predictions can help satellite internet providers:

- Manage service quality during adverse weather
- Proactively notify customers of potential disruptions
- Optimize transmission power and resource allocation

---

##  Technical Goals

- Collect weather data from public APIs
- Simulate satellite signal degradation using physics-inspired models
- Build and evaluate multiple regression algorithms
- Identify key weather factors affecting signal strength
- Create a reproducible, well-documented pipeline for portfolio demonstration

---

##  Tech Stack

- **Languages & Libraries**: `Python`, `pandas`, `numpy`, `scikit-learn`, `matplotlib`, `seaborn`, `xgboost`, `shap`, `requests`
- **APIs**: `OpenWeatherMap` (free tier)
- **Tools**: `Jupyter Notebook`, `PyCharm`, `Git`

---

##  Project Structure
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
├── src/ 
│  ├── data_collection.py # Weather API scripts
|  ├── data_validation.py  # for schema and quality checks
│  ├── signal_simulation.py # Signal strength simulation logic
│  ├── preprocessing.py # Data cleaning and feature engineering 
│  ├── modeling.py # Model training and evaluation
│  └── utils.py # Helper functions 
│ 
├── results/
│  ├── figures/ # Plots and visualizations 
│  ├── models/ # Saved model files
│  └── reports/ # Summary reports and metrics
│  
├── README.md # Project documentation
└── requirements.txt # Python dependencies
```