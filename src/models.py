from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, StackingRegressor
from xgboost import XGBRegressor
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

def get_model(name):
    if name == "lr":
        return LinearRegression()
    elif name == "rf":
        return RandomForestRegressor(n_estimators=100, random_state=42)
    elif name == "xgb":
        return XGBRegressor(n_estimators=100, random_state=42)
    elif name == "poly":
        return make_pipeline(PolynomialFeatures(degree=2), LinearRegression())
    elif name == "stack":
        return StackingRegressor(
            estimators=[
                ('lr', LinearRegression()),
                ('rf', RandomForestRegressor(n_estimators=100, random_state=42)),
                ('xgb', XGBRegressor(n_estimators=100, random_state=42))
            ],
            final_estimator=LinearRegression()
        )
    else:
        raise ValueError(f"Unknown model: {name}")
