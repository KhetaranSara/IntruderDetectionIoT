from sklearn.ensemble import IsolationForest
import numpy as np
import pandas as pd
import joblib  # ใช้ joblib แทน pickle เพื่อความเข้ากันได้ที่ดีกว่า

# โหลดข้อมูลของคุณ
# แทนที่ 'Merged_Ultrasonic_and_MatchFace_Data.csv' ด้วยชื่อไฟล์ของคุณ
data = pd.read_csv("Merged_Ultrasonic_and_MatchFace_Data.csv")

# เลือกฟีเจอร์ที่ต้องการใช้ในการฝึกโมเดล
X = data[['value_ultrasonic', 'value_matchface']].values

# สร้างและฝึกโมเดล Isolation Forest
model = IsolationForest(contamination=0.1, random_state=42)
model.fit(X)

# บันทึกโมเดลด้วย joblib
joblib.dump(model, "anomaly_detection_model.joblib")

print("Model trained and saved successfully as 'anomaly_detection_model.joblib'")
