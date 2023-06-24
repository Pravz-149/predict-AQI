import streamlit as st
import pandas as pd
import numpy as np
import joblib


best_model = joblib.load('best_model.pkl')

def main():
    st.title("AQI Prediction")
    st.write("Enter the pollutant concentrations below to predict the AQI.")

    # Create input fields for pollutant concentrations
    co = st.number_input("CO (in ppm)")
    no = st.number_input("NO (in ppb)")
    no2 = st.number_input("NO2 (in ppb)")
    o3 = st.number_input("O3 (in ppb)")
    so2 = st.number_input("SO2 (in ppb)")
    pm2_5 = st.number_input("PM2.5 (in µg/m³)")
    pm10 = st.number_input("PM10 (in µg/m³)")
    nh3 = st.number_input("NH3 (in ppb)")

    # Create a DataFrame with the input data
    input_data = pd.DataFrame(
        {
            "co": [co],
            "no": [no],
            "no2": [no2],
            "o3": [o3],
            "so2": [so2],
            "pm2_5": [pm2_5],
            "pm10": [pm10],
            "nh3": [nh3]
        }
    )

    # Make the AQI prediction using the best model
    predicted_aqi = best_model.predict(input_data)

    # Display the predicted AQI
    st.subheader("Predicted AQI")
    st.write(predicted_aqi[0])

if __name__ == "__main__":
    main()
