#from hopsworks import featurestore

#Retrieve the features from hopsworks
#df = featurestore.get_featuregroup("predict_aqi", version=1)

#since, the hopsworks is not being installed on vscode 
from api import get_aqi_data
df = get_aqi_data("Bengaluru")


import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
import xgboost as xgb
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_squared_error

df_rev = df[["dt", "co", "no", "no2", "o3", "so2", "pm2_5", "pm10", "nh3","AQI"]]

df_rev["dt"] = df_rev["dt"].astype('int64') // 10**9  # Convert to seconds

# Perform imputation on missing values
imputer = SimpleImputer(strategy='mean')  # You can choose an appropriate imputation strategy
df_imp = pd.DataFrame(imputer.fit_transform(df_rev), columns=df_rev.columns)

# Set the index to the date column
df_imp['dt'] = pd.to_datetime(df_imp['dt'])

# Filter the feature dataframe with input and output columns
input_cols = df_imp[["co", "no", "no2", "o3", "so2", "pm2_5", "pm10", "nh3"]]
output_col = df_imp["AQI"]

# Split the data into training and testing datasets
X_train, X_test, y_train, y_test = train_test_split(input_cols, output_col, test_size=0.2, random_state=42)

# Impute missing values with the mean
imputer = SimpleImputer(strategy='mean')
X_train = imputer.fit_transform(X_train)
X_test = imputer.transform(X_test)

# Initialize regression models
models = [
    LinearRegression(),
    DecisionTreeRegressor(),
    RandomForestRegressor(),
    xgb.XGBRegressor()
]

# Initialize the best model and minimum MSE
best_model = None
min_mse = np.inf

# Train and evaluate each model
for model in models:
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(model.__class__.__name__)
    print("Mean Squared Error:", mse)
    print()

    # Check if the current model has lower MSE than the minimum MSE
    if mse < min_mse:
        min_mse = mse
        best_model = model

# Print the best model
print("Best Model:", best_model.__class__.__name__)
print("Best Mean Squared Error:", min_mse)

# Save the best model
import joblib
joblib.dump(best_model, 'best_model.pkl')
