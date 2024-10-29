import csv
import os
from collections import Counter
import pandas as pd

# Replace this with the path to your directory containing CSV files
directory_path = '/home/tts/ttsteam/repos/oov_plus_plus/training_manifests'

# Prepare a list to store results
results = []

# Iterate through each file in the directory
for filename in os.listdir(directory_path):
    if filename.endswith('.csv'):
        # Construct full file path
        file_path = os.path.join(directory_path, filename)
        
        # Read the CSV file
        try:
            data = pd.read_csv(file_path, sep='|', header=None)
            # Count unique speakers in the third column (index 2)
            unique_speakers_count = data[2].nunique()
            # Append the result to the list
            results.append({'filename': filename, 'speaker_count': unique_speakers_count})
        except Exception as e:
            print(f"Error processing {filename}: {e}")

# Create a DataFrame from the results
result_df = pd.DataFrame(results)

# Save results to a new CSV file
result_file_path = os.path.join('/home/tts/ttsteam/repos/oov_plus_plus/scripts/table', 'unique_speaker_counts.csv')
result_df.to_csv(result_file_path, index=False)

print(f'Results saved to {result_file_path}')
