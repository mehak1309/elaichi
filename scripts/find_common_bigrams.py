import pandas as pd

# File paths
file1 = '/home/tts/ttsteam/repos/oov_plus_plus/bigrams/hin/bigrams_1.csv'
file2 = '/home/tts/ttsteam/repos/oov_plus_plus/bigrams/hin/bigrams_2.csv'
output_file = '/home/tts/ttsteam/repos/oov_plus_plus/bigrams/hin/common_bigrams/common_bigrams.csv'

# Read the CSV files
df1 = pd.read_csv(file1, header=None, names=['bigram', 'frequency_1'])
df2 = pd.read_csv(file2, header=None, names=['bigram', 'frequency_2'])

# Find common bigrams
common_bigrams = pd.merge(df1, df2, on='bigram')

# Add a new column with the maximum frequency
common_bigrams['max_frequency'] = common_bigrams[['frequency_1', 'frequency_2']].max(axis=1)
common_bigrams = common_bigrams.drop(columns=['frequency_1', 'frequency_2'])
common_bigrams = common_bigrams.sort_values(by='max_frequency', ascending=False)

# Save the result to a CSV file
common_bigrams.to_csv(output_file, index=False, header=False)

print(f"Common bigrams with maximum frequencies saved to {output_file}")
