import pandas as pd
import os
import json

json_file = '/home/tts/ttsteam/datasets/indicvoices_r/ivr_manifest_benchmark_splits/Hindi/metadata_train.json'
output_path = '/home/tts/ttsteam/repos/oov_plus_plus/sentences/hin/all_sentences.csv'

normalized_values = []

with open(json_file, 'r') as f:
    for line in f:
        try:
            # Parse each line as a JSON object
            item = json.loads(line)
            # Check if the 'lang' key is 'mr'
            if item.get('lang') == 'hi':
                # Append the 'normalized' value to the list
                normalized_values.append((item.get('filepath'), item.get('normalized'), item.get('gender')))
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")

# Output the list
pd.DataFrame(normalized_values).to_csv(output_path, header=None, index=False)