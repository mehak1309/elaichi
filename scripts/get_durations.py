# -*- coding: utf-8 -*-
"""
Calculates hours (.wav/.mp3) from a manifest file (CSV format, separated by |, 
with audio file paths in the first column)

Example usage:
    python calculate_durations.py -m manifest.csv -o durations_output.csv
"""

import os
import ffmpeg
import argparse
import pandas as pd
from tqdm import tqdm
import concurrent.futures

def get_duration(path):
    try:
        return float(ffmpeg.probe(path)['format']['duration'])
    except Exception as e:
        print(path)
        print(e)
        return 0


def run(args):
    # Read the manifest CSV
    df_manifest = pd.read_csv(args.manifest, sep='|', header=None, names = ['audio_filepath', 'text', 'speaker', 'emotion'])
    
    # Extract file paths from the first column
    filenames = df_manifest['audio_filepath'].tolist()
    print (filenames[0])
    durations = []
    with tqdm(total=len(filenames)) as pbar:
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.num_workers) as executor:
            futures = {executor.submit(get_duration, filename): filename for filename in filenames}
            results = {}
            for future in concurrent.futures.as_completed(futures):
                arg = futures[future]
                results[arg] = future.result()
                pbar.update(1)

    filenames = [f for f in results.keys()]
    durations = [d for d in results.values()]

    df = pd.DataFrame({'filename': filenames, 'duration': durations})
    df = df[df['duration'] > 0]  # Filter out files with 0 duration
    df.to_csv(args.output_csv, index=False)

    # Print quick statistics
    print (args.manifest)
    print('-'*20, 'QUICK_STATS', '-'*20)
    print(df.describe())
    print('-'*50)
    total_duration_hours = df['duration'].sum()/60/60
    total_duration_minutes = df['duration'].sum()/60
    print(f"{total_duration_hours:.2f} hours of data!")
    print(f"{total_duration_minutes:.2f} mins of data!")
    print('-'*50)

# 
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-m',
        '--manifest',
        type=str,
        required=True,
        help='Path to the manifest CSV file containing audio file paths.'
    )
    parser.add_argument(
        '-o',
        '--output_csv',
        type=str,
        default='durations.csv',
        help='Output CSV path with duration of each audio file found.')
    parser.add_argument(
        '-nw',
        '--num_workers',
        type=int,
        default=1,
        help='Number of workers used by ThreadPoolExecutor.'
    )
    args = parser.parse_args()
    run(args)
