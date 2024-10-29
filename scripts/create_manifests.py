import random
import pandas as pd

# Define the file path
filepath = '/home/tts/ttsteam/repos/oov_plus_plus/vits/manifests/indic-tts-30pct/metadata_test_cls.csv'
output_filepath = '/home/tts/ttsteam/repos/oov_plus_plus/vits/manifests/indic-tts-30pct/metadata_test_sample.csv'

# Read the CSV file
df = pd.read_csv(filepath, sep='|')

# Randomly select 30% of the rows
df_sample = df.sample(frac=0.3)

# Save the sampled rows to a new CSV
df_sample.to_csv(output_filepath, index=False, sep='|')

print(f'Selected 30% random rows and saved to {output_filepath}')
