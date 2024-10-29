import pandas as pd
import os

# Specify the directory containing the CSV files
directory_path = '/home/tts/ttsteam/repos/oov_plus_plus/training_manifests/train_and_test_1k.csv'  # Replace with your actual directory path
output_file_path = '/home/tts/ttsteam/repos/oov_plus_plus/scripts/table/testandtrain_duation.csv'  # Output CSV file

# Create an empty list to store the results
results = []

# Loop through each file in the specified directory
for filename in os.listdir(directory_path):
    if filename.endswith('.csv'):
        file_path = os.path.join(directory_path, filename)
        
        # Read the CSV file into a DataFrame
        data = pd.read_csv(file_path)
        
        # Sum the duration column
        total_duration_seconds = data['duration'].sum()

        total_duration = total_duration_seconds / 3600
        
        # Append the filename and total duration to the results list
        results.append({'filename': filename, 'total_duration': total_duration})

# Create a DataFrame from the results
results_df = pd.DataFrame(results)

# Write the results to a new CSV file, appending if it already exists
results_df.to_csv(output_file_path, index=False, header=not os.path.exists(output_file_path))

print(f'Total durations have been written to {output_file_path}.')
