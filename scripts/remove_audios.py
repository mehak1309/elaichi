import os
import pandas as pd

# Path to the input CSV file
input_csv_path = '/home/tts/ttsteam/repos/oov_plus_plus/scripts/test_manifests/only_ivr.csv'

# Path to the output CSV file
output_csv_path = '/home/tts/ttsteam/repos/oov_plus_plus/scripts/test_manifests/only_ivr.csv'

# Read the CSV file
df = pd.read_csv(input_csv_path, header=None, sep='|')

# Check if the .wav files exist and filter the DataFrame
df_filtered = df[df[0].apply(lambda x: os.path.exists(x))]

# Save the filtered DataFrame to a new CSV file
df_filtered.to_csv(output_csv_path, index=False, header=False, sep='|')

print(f"Filtered CSV saved to {output_csv_path}")
