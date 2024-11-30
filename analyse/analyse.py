import requests
import numpy as np
#import pickle
import joblib
import time

# โหลดโมเดลที่บันทึกไว้จากไฟล์

model = joblib.load("anomaly_detection_model.joblib")

# ข้อมูลการเชื่อมต่อ Adafruit IO
ADAFRUIT_IO_USERNAME = "65050101"  # ระบุชื่อผู้ใช้ของ Adafruit IO
ADAFRUIT_IO_KEY = "aio_rtaT32P6zBe87LXT5Iz9fsrjFrkB"            # ระบุ API Key ของ Adafruit IO
ULTRASONIC_FEED_URL = f"https://io.adafruit.com/api/v2/65050101/feeds/ultrasonic/data"
MATCHFACE_FEED_URL = f"https://io.adafruit.com/api/v2/65050101/feeds/matchface/data"
ANOMALY_STATUS_FEED_URL = f"https://io.adafruit.com/api/v2/65050101/feeds/anomaly-status/data"

# ฟังก์ชันในการดึงข้อมูลล่าสุดจาก Adafruit IO
def fetch_latest_data(feed_url):
    headers = {
        'X-AIO-Key': ADAFRUIT_IO_KEY,
    }
    response = requests.get(feed_url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return int(data[0]["value"])
    else:
        print(f"Error fetching data: {response.status_code}")
        return None

# ฟังก์ชันในการอัปเดตสถานะความผิดปกติไปยัง Adafruit IO
def update_anomaly_status(status):
    headers = {
        'X-AIO-Key': ADAFRUIT_IO_KEY,
    }
    payload = {"value": status}
    response = requests.post(ANOMALY_STATUS_FEED_URL, headers=headers, json=payload)
    if response.status_code == 200:
        print(f"Updated status to: {status}")
    else:
        print(f"Error updating status: {response.status_code}")

# เริ่มการตรวจจับความผิดปกติแบบเรียลไทม์
while True:
    # ดึงข้อมูล ultrasonic และ matchFace ล่าสุดจาก Adafruit IO
    ultrasonic_value = fetch_latest_data(ULTRASONIC_FEED_URL)
    matchface_value = fetch_latest_data(MATCHFACE_FEED_URL)
    
    if ultrasonic_value is not None and matchface_value is not None:
        # สร้างข้อมูลสำหรับทำนาย
        data_point = np.array([[ultrasonic_value, matchface_value]])
        
        # ทำนายความผิดปกติด้วยโมเดลที่บันทึกไว้
        prediction = model.predict(data_point)
        
        if prediction == -1:
            print("Anomaly Detected! Unusual activity found.")
            update_anomaly_status("Anomaly")  # ส่งสถานะ "ผิดปกติ" ไปยัง Adafruit IO
        else:
            print("Normall Activity.")
            update_anomaly_status("normal")  # ส่งสถานะ "ปกติ" ไปยัง Adafruit IO
    
    # หน่วงเวลาสำหรับการดึงข้อมูลรอบถัดไป (ปรับให้เหมาะสมกับความถี่ของข้อมูล)
    time.sleep(10)
