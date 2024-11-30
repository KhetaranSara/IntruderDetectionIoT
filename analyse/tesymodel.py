import joblib
import numpy as np

# โหลดโมเดล
model = joblib.load("anomaly_detection_model.joblib")

# ตัวอย่างการทำนายความผิดปกติ
# ใส่ค่า ultrasonic และ matchFace ที่ได้รับจาก Adafruit IO
data_point = np.array([[1, 1]])  # ตัวอย่างค่า input (เช่น ultrasonic=1, matchFace=-1)

# ทำนาย
prediction = model.predict(data_point)

# ตรวจสอบผลลัพธ์
if prediction == -1:
    print("Anomaly Detected! Unusual activity found.")
else:
    print("Normal activity.")
