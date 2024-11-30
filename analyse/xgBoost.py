import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.utils import resample
from xgboost import XGBClassifier
import numpy as np

# Step 1: Load and prepare the data
# Load the dataset you uploaded
file_path = 'Updated_Balanced_MatchFace_Processed.csv'
data = pd.read_csv(file_path)

# Step 2: Balance the data
# Separate majority and minority classes
class_0 = data[data['value_matchface'] == 0]
class_non_0 = data[data['value_matchface'] != 0]

# Downsample class 0 but keep more samples (2x the size of the smaller classes)
class_0_downsampled = resample(
    class_0,
    replace=False,
    n_samples=len(class_non_0) * 2,  # Keep 2x the size of the smaller classes
    random_state=42
)

# Combine the downsampled majority class with the minority classes
balanced_data = pd.concat([class_0_downsampled, class_non_0])

# Split into features and target
X_balanced = balanced_data[['hour', 'value_ultrasonic']]
y_balanced = balanced_data['value_matchface']

# Step 3: Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X_balanced, y_balanced, test_size=0.2, random_state=42, stratify=y_balanced
)

# Step 4: Train the XGBoost model
# Map labels to integers for XGBoost
label_mapping = {-1: 0, 0: 1, 1: 2}
inverse_label_mapping = {v: k for k, v in label_mapping.items()}

# Automatically handle any unknown labels in y_test
unique_labels = set(y_test.unique())
for label in unique_labels:
    if label not in label_mapping:
        # Assign a new mapping for unknown labels
        next_label_id = max(label_mapping.values()) + 1
        label_mapping[label] = next_label_id
        inverse_label_mapping[next_label_id] = label

# Debugging: Ensure -1 mapping exists
if -1 not in label_mapping:
    label_mapping[-1] = max(label_mapping.values()) + 1
    inverse_label_mapping[label_mapping[-1]] = -1

# Debugging: Print label mappings
print("Label Mapping:", label_mapping)
print("Inverse Label Mapping:", inverse_label_mapping)

# Create and train the model
xgb_model = XGBClassifier(
    random_state=42,
    use_label_encoder=False,
    eval_metric='mlogloss',
    n_estimators=50,  # Number of boosting rounds
    max_depth=3,  # Maximum tree depth
    learning_rate=0.1  # Learning rate
)
xgb_model.fit(X_train, y_train.map(label_mapping))

# Step 5: Predict for hours 0-23 with ultrasonic=1
test_hours = np.array([[hour, 1] for hour in range(24)])
predicted_classes = xgb_model.predict(test_hours)

# Map predictions back to original labels
predicted_classes_original = pd.Series(predicted_classes).map(inverse_label_mapping)

# Combine predictions for readability
prediction_results = {hour: prediction for hour, prediction in zip(range(24), predicted_classes_original)}

# Step 6: Evaluate the model
# Map test labels and predictions back to original labels
y_test_original = y_test.map(label_mapping).map(inverse_label_mapping)

# Check for NaN in y_test_original
if y_test_original.isna().any():
    problematic_values = y_test[y_test_original.isna()]
    print("NaN found in y_test_original. Problematic values in y_test:")
    print(problematic_values)
else:
    # Predict on the test set
    y_pred_test = xgb_model.predict(X_test)
    y_pred_test_original = pd.Series(y_pred_test).map(inverse_label_mapping)

    # Calculate accuracy and classification report
    accuracy = accuracy_score(y_test_original, y_pred_test_original)
    classification_report_result = classification_report(y_test_original, y_pred_test_original, zero_division=0)

    # Outputs
    print("Prediction Results for Hours 0-23 with Ultrasonic=1:")
    print(prediction_results)
    print("\nModel Accuracy:", accuracy)
    print("\nClassification Report:\n", classification_report_result)
