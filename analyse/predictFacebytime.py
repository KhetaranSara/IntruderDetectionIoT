import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
data_path = 'Date_and_Time_Separated_Data.csv'
data = pd.read_csv(data_path)

# Preprocess data to extract hour from time and prepare features and target
data['hour'] = pd.to_datetime(data['time'], format="%H:%M:%S").dt.hour  # Extract hour from time
X = data[['value_ultrasonic', 'hour']]  # Use ultrasonic and hour as features
y = data['value_matchface']  # Target variable

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the Random Forest model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Function to predict a single instance
def predict_single(value_ultrasonic, hour):
    input_data = pd.DataFrame({'value_ultrasonic': [value_ultrasonic], 'hour': [hour]})
    prediction = model.predict(input_data)
    return prediction[0]

# Example of single prediction
value_ultrasonic = 1  # Example value for ultrasonic
hour = 13  # Example hour
predicted_matchFace = predict_single(value_ultrasonic, hour)
print("การทำนายคือ", predicted_matchFace)

# Model evaluation metrics
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='weighted', zero_division=1)
recall = recall_score(y_test, y_pred, average='weighted')
f1 = f1_score(y_test, y_pred, average='weighted')
conf_matrix = confusion_matrix(y_test, y_pred)

print(f"Accuracy: {accuracy * 100:.2f}%")
print(f"Precision: {precision:.2f}")
print(f"Recall: {recall:.2f}")
print(f"F1 Score: {f1:.2f}")
# Plotting the Confusion Matrix as a heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', cbar=False, 
            xticklabels=['-1 (Stranger)', '0 (No Scan)', '1 (Known)'], 
            yticklabels=['-1 (Stranger)', '0 (No Scan)', '1 (Known)'])
plt.xlabel('Predicted Labels')
plt.ylabel('True Labels')
plt.title('Confusion Matrix for Random Forest Model Performance')
plt.show()

# Output the results
predicted_matchFace, accuracy, precision, recall, f1
