# predict-AIQ
Title: Predict Air Quality Index (AQI) in your City

Objective: To develop an AQI app that provides real-time information, precautions
By taking the historical raw data of pollutants

Plan Implementation and Execution Process:
1. Data Collection: Gather historical and real-time data on pollutant concentrations from reliable sources from https://openweathermap.org/api
2. Data Preprocessing: Handling Missing Values, Set Date Index, Outliers etc
3. AQI Calculation: Calculate the AQI based on pollutant concentrations - built functions
4. User Interface: Design a user-friendly interface to present the AQI information, precautions, and forecasted data.
5. Model Training: Developed a script to train the model using the pollutant AQI as features and the resultant AQI as the target. Random Forest Regressor performed best 
6. Automation: Created a separate script to automate data fetching and training processes.
7. Deployment: Deployed the model on a Streamlit app and hosted on GitHub.

Blockers and Alternatives:
1. Hops Work Integration:
   - Initially attempted to install the required features into Hops Work for seamless integration.
   - Encountered an issue during installation in Visual Studio Code, which couldn't be resolved within the given time frame.
2. Alternative Approach:
   - Due to time constraints, I decided to automate the data fetching and training process without pushing and pulling data from the feature store.
   - Adapted the workflow to fetch data from the openweather.org API directly.

Assumptions:
1. The app assumes the availability of reliable data sources for pollutant concentrations.
2. The accuracy of the AQI calculations and the forecasting models depends on the quality and accuracy of the input data.
3. The app assumes users will input accurate pollutant concentrations for manual entry.

App Working Process(https://pravz-149-predict-aqi-app-1yu5zc.streamlit.app/):
1. User selects a date or manually enters pollutant concentrations.
2. If a date is selected, the app retrieves the corresponding AQI category and recommends precautions.
3. If no date is selected, the user can input pollutant concentrations manually.
4. The app calculates the AQI and displays the category along with precautions.
5. The forecasted data is presented to the user, allowing them to plan activities accordingly.

Results:
1. Users can access real-time AQI information and precautions for specific dates.
2. Users can manually enter pollutant concentrations if desired date data is not available.

Limitations:
1. Limited availability of historical and real-time data on pollutant concentrations.
2. Complexities in implementing time series forecasting models for accurate predictions.

