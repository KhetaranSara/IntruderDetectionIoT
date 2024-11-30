import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

# Load the dataset
file_path = 'Updated_Balanced_MatchFace_Processed.csv'
data = pd.read_csv(file_path)

# Convert 'created_at' column to datetime
data['datetime'] = pd.to_datetime(data['created_at'])

# Filter data for intruders only (value_matchface = -1)
intruder_data = data[data['value_matchface'] == -1]

# Aggregate data to hourly frequency
intruder_trend = intruder_data.set_index('datetime').resample('h').size().reset_index()
intruder_trend.columns = ['ds', 'y']  # Prophet requires columns 'ds' and 'y'

# Fill missing values with 0
intruder_trend['y'] = intruder_trend['y'].fillna(0)

# Initialize the Prophet model
model = Prophet()
model.fit(intruder_trend)

# Create future dataframe for the next 72 hours
future = model.make_future_dataframe(periods=72, freq='H')
forecast = model.predict(future)

# Plot the forecast
fig = model.plot(forecast)
plt.title("Intruder Trend Prediction by Hour (Prophet)")
plt.xlabel("Datetime")
plt.ylabel("Frequency of Intruder Detection")
plt.show()

# Optional: Plot forecast components (trend, weekly, yearly seasonality)
fig2 = model.plot_components(forecast)
plt.show()




from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt

# Fit ARIMA model
model = ARIMA(intruder_trend['y'], order=(5, 1, 0))  # Adjust (p, d, q) as needed
arima_model = model.fit()

# Forecast the next 72 hours
forecast = arima_model.forecast(steps=72)
forecast_index = pd.date_range(start=intruder_trend['ds'].iloc[-1], periods=72, freq='H')

# Plot the results
plt.figure(figsize=(14, 7))
plt.plot(intruder_trend['ds'], intruder_trend['y'], label='Historical Data')
plt.plot(forecast_index, forecast, label='Forecast', color='red')
plt.title("Intruder Trend Prediction by Hour (ARIMA)")
plt.xlabel("Datetime")
plt.ylabel("Frequency of Intruder Detection")
plt.legend()
plt.grid()
plt.show()
