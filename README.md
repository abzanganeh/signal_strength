# Satellite Signal Strength Prediction
A Supervised Regression Project for Predicting Signal Quality Based on Weather Conditions

## Overview
This project develops machine learning models to predict satellite signal strength (in dBm) based on weather conditions and atmospheric factors.  
It follows a structured learning path:
1. **Simple Linear Regression** – one feature (rain rate)
2. **Multiple Regression** – multiple weather features
3. **Non-linear Models** – Random Forest, XGBoost
4. **Advanced Optimization** – feature engineering, hyperparameter tuning

**Business Relevance:** Accurate predictions can help satellite internet providers manage service quality, proactively notify customers, and optimize transmission power during adverse weather.

## Technical Goals
- Collect weather data from public APIs
- Simulate satellite signal degradation based on physical models
- Build and evaluate multiple regression algorithms
- Identify key weather factors affecting signal strength
- Create reproducible, well-documented analysis for portfolio demonstration

## Tech Stack
- **Python**: pandas, numpy, scikit-learn, matplotlib, seaborn, xgboost, shap, requests
- **APIs**: OpenWeatherMap (free tier)
- **Tools**: Jupyter Notebook, PyCharm, Git

## Project Structure
data/ # Raw and processed datasets
notebooks/ # Jupyter experiments
src/ # Data collection, simulation, preprocessing, modeling, evaluation
results/ # Figures, trained models, reports
README.md # Project documentation
requirements.txt # Dependencies