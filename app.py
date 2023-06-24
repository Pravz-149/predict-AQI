import streamlit as st
import pandas as pd
import joblib
from datetime import date
from api import get_aqi_data

# Load the trained model
model = joblib.load('best_model.pkl')

# Define the feature names or columns used by the model
feature_cols = ["co", "no", "no2", "o3", "so2", "pm2_5", "pm10", "nh3"]

def get_aqi_category(aqi):
    if aqi <= 50:
        return "Good"
    elif aqi <= 100:
        return "Moderate"
    elif aqi <= 150:
        return "Unhealthy for Sensitive Groups"
    elif aqi <= 200:
        return "Unhealthy"
    elif aqi <= 300:
        return "Very Unhealthy"
    else:
        return "Hazardous"

def get_health_implications(aqi_category):
    if aqi_category == "Good":
        return "Air quality is considered satisfactory, and air pollution poses little or no risk."
    elif aqi_category == "Moderate":
        return "Air quality is acceptable, but there may be a moderate health concern for a very small number of individuals."
    elif aqi_category == "Unhealthy for Sensitive Groups":
        return "Members of sensitive groups may experience health effects. The general public is less likely to be affected."
    elif aqi_category == "Unhealthy":
        return "Some members of the general public may experience health effects. Sensitive individuals are at a higher risk."
    elif aqi_category == "Very Unhealthy":
        return "Health alert: The risk of health effects is increased for everyone."
    else:
        return "Health warning of emergency conditions: The entire population is more likely to be affected."

def predict_aqi(features, selected_date):
    # Fetch the data for Bengaluru from the API
    df = get_aqi_data("Bengaluru")
    
    input_data = pd.DataFrame([features], columns=feature_cols)
    prediction = model.predict(input_data)
    
    # Filter the AQI details for the selected date
    aqi_details = df[df['dt'].dt.date == selected_date]
    return prediction[0], aqi_details

def main():

    st.title("Predict the Air Quality Index in Bengaluru")

    df = get_aqi_data("Bengaluru")

    # Get the current date
    current_date = date.today().strftime("%B %d, %Y")

    # Get the AQI details for today
    aqi_details_today = df[df['dt'].dt.date == date.today()]

    # Display the AQI details for today
    st.subheader("AQI Details for Today")
    if not aqi_details_today.empty:
        st.write(aqi_details_today)
    else:
        st.write("No AQI data available for today. Please enter the Pollutant Concentrations to predict the AQI")

    # Add input fields for pollutant concentrations and date
    st.subheader("Enter the Pollutant Concentrations")

    # Check if selected date exists in the DataFrame
    existing_dates = df['dt'].dt.date.unique()
    selected_date = st.date_input("Select a Date")


    if selected_date in existing_dates:
        # Pre-fill the pollutant concentration values for the selected date
        selected_row = df[df['dt'].dt.date == selected_date].iloc[0]
        default_values = {
            "co": selected_row['co'],
            "no": selected_row['no'],
            "no2": selected_row['no2'],
            "o3": selected_row['o3'],
            "so2": selected_row['so2'],
            "pm2_5": selected_row['pm2_5'],
            "pm10": selected_row['pm10'],
            "nh3": selected_row['nh3']
        }

        co = st.number_input("CO (in µg/m³)", min_value=0.0, step=0.01, value=default_values['co'])
        no = st.number_input("NO (in µg/m³)", min_value=0.0, step=0.01, value=default_values['no'])
        no2 = st.number_input("NO2 (in µg/m³)", min_value=0.0, step=0.01, value=default_values['no2'])
        o3 = st.number_input("O3 (in µg/m³)", min_value=0.0, step=0.01, value=default_values['o3'])
        so2 = st.number_input("SO2 (in µg/m³)", min_value=0.0, step=0.01, value=default_values['so2'])
        pm2_5 = st.number_input("PM2.5 (in µg/m³)", min_value=0.0, step=0.1, value=default_values['pm2_5'])
        pm10 = st.number_input("PM10 (in µg/m³)", min_value=0.0, step=0.1, value=default_values['pm10'])
        nh3 = st.number_input("NH3 (in µg/m³)", min_value=0.0, step=0.01, value=default_values['nh3'])
    else:
        # Ask the user to enter pollutant concentration values
        co = st.number_input("CO (in ppm)", min_value=0.0, step=0.01)
        no = st.number_input("NO (in ppm)", min_value=0.0, step=0.01)
        no2 = st.number_input("NO2 (in ppm)", min_value=0.0, step=0.01)
        o3 = st.number_input("O3 (in ppm)", min_value=0.0, step=0.01)
        so2 = st.number_input("SO2 (in ppm)", min_value=0.0, step=0.01)
        pm2_5 = st.number_input("PM2.5 (in µg/m³)", min_value=0.0, step=0.1)
        pm10 = st.number_input("PM10 (in µg/m³)", min_value=0.0, step=0.1)
        nh3 = st.number_input("NH3 (in ppm)", min_value=0.0, step=0.01)

    # Button to generate AQI prediction
    if st.button("Generate AQI"):
        # Perform the AQI prediction
        input_features = {
            "co": co,
            "no": no,
            "no2": no2,
            "o3": o3,
            "so2": so2,
            "pm2_5": pm2_5,
            "pm10": pm10,
            "nh3": nh3
        }
        if selected_date in existing_dates:
            prediction, aqi_details = predict_aqi(input_features, selected_date)

            # Display the result message
            st.subheader("AQI Prediction")
            if not aqi_details.empty:
                st.write(f"The AQI for Bengaluru on {selected_date} with the mentioned pollutant concentrations is:")
                st.write(prediction)

                # Display AQI category and health implications
                aqi_category = get_aqi_category(prediction)
                health_implications = get_health_implications(aqi_category)

                st.subheader("AQI Category")
                st.write(aqi_category)

                st.subheader("Health Implications")
                st.write(health_implications)
        else:
            st.write(f"No AQI data available for {selected_date}. Using the model to generate the AQI.")

            # Calculate AQI using the model without actual data
            prediction = model.predict(pd.DataFrame([input_features], columns=feature_cols))[0]

            # Display the result message
            st.subheader("AQI Prediction")
            st.write(f"The AQI for Bengaluru on {selected_date} with the entered pollutant concentrations is:")
            st.write(prediction)

            # Display AQI category and health implications
            aqi_category = get_aqi_category(prediction)
            health_implications = get_health_implications(aqi_category)

            st.subheader("AQI Category")
            st.write(aqi_category)

            st.subheader("Health Implications")
            st.write(health_implications)

if __name__ == "__main__":
    main()    