import requests
import pandas as pd
import aqi
#import hopsworks
from geopy.geocoders import Nominatim
from datetime import datetime, timezone

def get_aqi_data(location_name):
    

    geolocator = Nominatim(user_agent="my_geocoder")
    location = geolocator.geocode(location_name)
    latitude = location.latitude
    longitude = location.longitude

    # API endpoint URL
    url = "http://api.openweathermap.org/data/2.5/air_pollution/history"

    # Parameters for the API request
    params = {
        "lat": latitude,   # Latitude of Bengaluru
        "lon": longitude,   # Longitude of Bengaluru
        "start": int(datetime(2015, 1, 1).replace(tzinfo=timezone.utc).timestamp()),   # Start timestamp
        "end": int(datetime.now().replace(tzinfo=timezone.utc).timestamp()),   # End timestamp
        "appid": "a1628122cfe7168773dd945517b21737"  # Replace with your actual API key
    }

    # Send the GET request
    response = requests.get(url, params=params)

    # Check the response status code
    if response.status_code == 200:
        # Successful request
        data = response.json()
        # Process the data as needed
        print("Data Collected Successfully")
    else:
        # Error in the request
        print("Error:", response.status_code)

    data_list = data["list"]

    columns = ["dt", "aqi", "co", "no", "no2", "o3", "so2", "pm2_5", "pm10", "nh3"]
    data = [[item["dt"], item["main"]["aqi"], *item["components"].values()] for item in data_list]


    # Create DataFrame
    df = pd.DataFrame(data, columns=columns)

    # Convert "dt" column to date format
    df["dt"] = pd.to_datetime(df["dt"], unit="s")

    # Set 'dt' column as the index of the DataFrame
    df.set_index('dt', inplace=True)

    # Resample to daily data
    df_daily = df.resample('D').mean()

    # Reset the index to have 'dt' as a column again
    df_daily = df_daily.reset_index()

    # Sort DataFrame by date in descending order
    df = df_daily.sort_values(by="dt", ascending=False)

    df.rename(columns={'aqi': 'aqi_avg_index'}, inplace=True)

    # Replace NaN values with mean using fillna()
    df = df.fillna(df.mean(numeric_only=True))


    def pm25_aqi(concentration, pollutant):
        concentration = str(round(float(concentration)))
        iaqi = aqi.to_iaqi(aqi.POLLUTANT_PM25, concentration, algo=aqi.ALGO_EPA)
        return iaqi

    def pm10_aqi(concentration, pollutant):
        concentration = str(round(float(concentration)))
        iaqi = aqi.to_iaqi(aqi.POLLUTANT_PM10, concentration, algo=aqi.ALGO_EPA)
        return iaqi

    def o3_aqi(concentration, pollutant):
        concentration = str(round(float(concentration)))
        iaqi = aqi.to_iaqi(aqi.POLLUTANT_O3_1H, concentration, algo=aqi.ALGO_EPA)
        return iaqi


    def no2_aqi(concentration, pollutant):
        concentration = str(round(float(concentration)))
        iaqi = aqi.to_iaqi(aqi.POLLUTANT_NO2_1H, concentration, algo=aqi.ALGO_EPA)
        return iaqi

    def so2_aqi(concentration, pollutant):
        concentration = str(round(float(concentration)))
        iaqi = aqi.to_iaqi(aqi.POLLUTANT_SO2_1H, concentration, algo=aqi.ALGO_EPA)
        return iaqi

    df['pm25_AQI'] = df['pm2_5'].apply(lambda x: pm25_aqi(x, 'pm25'))
    df['pm10_AQI'] = df['pm10'].apply(lambda x: pm10_aqi(x, 'pm10'))
    #df['o3_AQI'] = df['o3'].apply(lambda x: pm10_aqi(x, 'o3'))
    df['so2_AQI'] = df['so2'].apply(lambda x: so2_aqi(x, 'so2'))
    df['no2_AQI'] = df['no2'].apply(lambda x: no2_aqi(x, 'no2'))

    aqi_columns = ['pm25_AQI', 'pm10_AQI', 'o3_AQI', 'so2_AQI', 'no2_AQI']
    df[aqi_columns] = df[aqi_columns].apply(pd.to_numeric, errors='coerce')
    df['AQI'] = df[aqi_columns].max(axis=1)

    df["AQI_Category"] = df["AQI"].apply(
        lambda x: "Good" if x <= 50 else
        "Satisfactory" if x <= 100 else
        "Moderate" if x <= 200 else
        "Poor" if x <= 300 else
        "Very Poor" if x <= 400 else
        "Severe"
    )

    print("Size of the Resulting Dataframe",df.shape)

    return df



    # ## creating feature groups
    # project = hopsworks.login()
    # fs = project.get_feature_store()

    # aqi_fg = fs.create_feature_group(
    #     name="predict_aqi",
    #     version=1,
    #     description="Air Quality and Pollutants Data with Pollutants aqi",
    #     primary_key=["dt"],
    #     event_time="dt"
    # )

    # aqi_fg.insert(df, write_options={"wait_for_job": False})

    # feature_descriptions = [
    #     {"name": "", "description": "Date and time"},
    #     {"name": "aqi_avg_index", "description": "Air Quality Index. Possible values: 1, 2, 3, 4, 5 which is resampled"},
    #     {"name": "co", "description": "concentration of CO (Carbon monoxide)"},
    #     {"name": "no", "description": "concentration of NO (Nitrogen monoxide)"},
    #     {"name": "no2", "description": "concentration of NO2 (Nitrogen dioxide)"},
    #     {"name": "o3", "description": "concentration of O3 (Ozone)"},
    #     {"name": "so2", "description": "concentration of SO2 (Sulphur dioxide)"},
    #     {"name": "pm2_5", "description": "concentration of PM2.5 (Fine particles matter)"},
    #     {"name": "pm10", "description": "concentration of PM10 (Coarse particulate matter)"},
    #     {"name": "nh3", "description": "concentration of NH3 (Ammonia)"},
    #     {"name": 'pm25_aqi', "description": "AQI value calculated from PM2.5 concentration"},
    #     {"name": 'pm10_aqi', "description": "AQI value calculated from PM10 concentration"},
    #     {"name": 'o3_aqi', "description": "AQI value calculated from O3 concentration"},
    #     {"name": 'so2_aqi', "description": "AQI value calculated from SO2 concentration"},
    #     {"name": 'no2_aqi', "description": "AQI value calculated from NO2 concentration"},
    #     {"name": 'aqi', "description": "Overall AQI value"},
    #     {"name": 'aqi_category', "description": "AQI category based on the overall AQI value"},
    # ]

    # for desc in feature_descriptions: 
    #     aqi_fg.update_feature_description(desc["name"], desc["description"])
