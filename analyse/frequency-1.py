import pandas as pd

# Load the uploaded CSV file to inspect its content
file_path = 'Updated_Balanced_MatchFace_Processed.csv'
data = pd.read_csv(file_path)

# Display the first few rows of the dataset to understand its structure
data.head()

import matplotlib.pyplot as plt

# Filter data where matchFace equals -1
matchface_negative = data[data['value_matchface'] == -1]
matchface_positive = data[data['value_matchface'] == 1]
# Count occurrences of matchFace = -1 per hour
hourly_counts_negative = matchface_negative['hour'].value_counts().sort_index()
hourly_counts_positive = matchface_positive['hour'].value_counts().sort_index()
# Plot the data as a bar chart
plt.figure(figsize=(10, 6))
plt.bar(hourly_counts_negative.index, hourly_counts_negative.values, width=0.8)
plt.bar(hourly_counts_positive.index, hourly_counts_positive.values, width=0.8)
plt.xlabel('Hour of the Day', fontsize=12)
plt.ylabel('Frequency of matchFace', fontsize=12)
plt.title('Frequency of matchFace by Hour of the Day', fontsize=14)
plt.xticks(range(0, 24), fontsize=10)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()
