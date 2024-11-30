
#####  ARIMA   ######

# import pandas as pd
# from statsmodels.tsa.arima.model import ARIMA
# import matplotlib.pyplot as plt

# # โหลดข้อมูล
# data = pd.read_csv("Merged_Ultrasonic_and_MatchFace_Data.csv")

# # แปลงคอลัมน์ 'created_at' ให้เป็น datetime
# data['created_at'] = pd.to_datetime(data['created_at'])

# # ดึงเฉพาะเวลาจาก 'created_at' และสร้างคอลัมน์ใหม่ที่ชื่อว่า 'time_only'
# data['time_only'] = data['created_at'].dt.time

# # กรองข้อมูลเพื่อเลือกเฉพาะคนแปลกหน้า (matchFace = -1)
# stranger_data = data[data['value_matchface'] == -1]

# # สร้าง Series ที่นับจำนวนการพบคนแปลกหน้าในแต่ละชั่วโมงของวัน (เช่น 08:00, 09:00, ...)
# stranger_trend = stranger_data.groupby(stranger_data['created_at'].dt.hour).size()

# # แปลงข้อมูลให้อยู่ในรูปแบบที่ต่อเนื่อง
# stranger_trend = stranger_trend.reindex(range(24), fill_value=0)  # เติมค่า 0 หากบางชั่วโมงไม่มีคนแปลกหน้า

# # แบ่งข้อมูลออกเป็นข้อมูลฝึก (train) และทดสอบ (test)
# train_data = stranger_trend[:int(0.8*len(stranger_trend))]
# test_data = stranger_trend[int(0.8*len(stranger_trend)):]

# # สร้างและฝึกโมเดล ARIMA
# model = ARIMA(train_data, order=(1, 1, 1))  # ปรับค่า (p, d, q) ตามความเหมาะสม
# model_fit = model.fit()

# # ทำนายข้อมูลในช่วงเวลาของ test data
# forecast = model_fit.forecast(steps=len(test_data))

# # แสดงผลการพยากรณ์
# plt.figure(figsize=(14, 7))
# plt.plot(train_data, label="Training Data")
# plt.plot(test_data, label="Test Data", color='orange')
# plt.plot(test_data.index, forecast, label="Forecasted Trend", color='green')
# plt.xlabel('Hour of the Day')
# plt.ylabel('Frequency of Stranger Detection')
# plt.title('Stranger Trend Prediction by Hour')
# plt.legend()
# plt.show()


##### prophet #####
# import pandas as pd
# from prophet import Prophet
# import matplotlib.pyplot as plt

# # โหลดข้อมูล
# data = pd.read_csv("Merged_Ultrasonic_and_MatchFace_Data.csv")

# # แปลงคอลัมน์ 'created_at' ให้เป็น datetime และลบ timezone
# data['created_at'] = pd.to_datetime(data['created_at']).dt.tz_localize(None)

# # กรองข้อมูลเพื่อเลือกเฉพาะคนแปลกหน้า (matchFace = -1)
# stranger_data = data[data['value_matchface'] == -1]

# # สร้าง DataFrame ใหม่ที่มีเฉพาะคอลัมน์ 'ds' (วันที่และเวลา) และ 'y' (จำนวนการพบคนแปลกหน้า)
# stranger_trend = stranger_data.set_index('created_at').resample('H').size().reset_index()
# stranger_trend.columns = ['ds', 'y']  # Prophet ต้องการให้คอลัมน์เวลาเป็น 'ds' และข้อมูลเป็น 'y'

# # เติมค่า 0 ในช่วงเวลาที่ไม่มีข้อมูล
# stranger_trend['y'] = stranger_trend['y'].fillna(0)

# # กรองข้อมูลเฉพาะช่วงเวลาที่คุณมีข้อมูล เช่น 0:00 - 8:00 (ไม่รวม 9:00-22:00)
# stranger_trend = stranger_trend[stranger_trend['ds'].dt.hour < 9]

# # สร้างและฝึกโมเดล Prophet
# model = Prophet()
# model.fit(stranger_trend)

# # พยากรณ์ข้อมูลในอนาคต
# future = model.make_future_dataframe(periods=24, freq='h')  # ใช้ 'h' แทน 'H'
# forecast = model.predict(future)

# # แสดงผลการพยากรณ์
# fig = model.plot(forecast)
# plt.title("Stranger Trend Prediction by Hour with Prophet")
# plt.xlabel("Hour of the Day")
# plt.ylabel("Frequency of Stranger Detection")
# plt.show()


import pandas as pd
from prophet import Prophet
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np
import matplotlib.pyplot as plt

# Load data
data = pd.read_csv("Date_and_Time_Separated_Data.csv")
#data = pd.read_csv("Updated_Balanced_MatchFace_Processed.csv")

# Convert date and time columns to datetime
data['datetime'] = pd.to_datetime(data['date'] + ' ' + data['time'])

# Filter data for strangers only (assuming 'value_matchface' = -1 indicates a stranger)
stranger_data = data[data['value_matchface'] == -1]

# Create DataFrame for Prophet with 'ds' and 'y' columns
stranger_trend = stranger_data.set_index('datetime').resample('h').size().reset_index()
stranger_trend.columns = ['ds', 'y']

# Fill missing values with 0 for hours with no stranger detections
stranger_trend['y'] = stranger_trend['y'].fillna(0)

# Initialize and fit Prophet model
model = Prophet(changepoint_prior_scale=0.1)
model.fit(stranger_trend)

# Create future dataframe and forecast
future = model.make_future_dataframe(periods=24, freq='h')
forecast = model.predict(future)

# Extract actual values for comparison (using last 10 hours as test data)
y_true = stranger_trend['y'][-10:].values
y_pred = forecast['yhat'][-10:].values

# Calculate performance metrics
mae = mean_absolute_error(y_true, y_pred)
mse = mean_squared_error(y_true, y_pred)
rmse = np.sqrt(mse)

# Print performance metrics
print(f"Mean Absolute Error (MAE): {mae}")
print(f"Mean Squared Error (MSE): {mse}")
print(f"Root Mean Squared Error (RMSE): {rmse}")

# Plot forecast with Prophet
fig, ax = plt.subplots(figsize=(14, 7))
model.plot(forecast, ax=ax)
ax.set_title("Stranger Trend Prediction by Hour with Prophet")
ax.set_xlabel("Time")
ax.set_ylabel("Frequency of Stranger Detection")

# Show the plot
plt.show()
