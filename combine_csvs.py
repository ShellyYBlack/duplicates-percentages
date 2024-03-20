# This will recursively walk a directory and combine CSVs into one CSV.

import pandas as pd
import os
from glob import glob

folder_path = "/syblack/Downloads/siegfried_csv_source_37485"
csv_files = os.walk(folder_path)
extension = "*.csv"
csv_files = [file
                 for path, subdir, files in os.walk(folder_path)
                 for file in glob(os.path.join(path, extension))]

# Create a list to hold the dataframes
df_list = []

for csv in csv_files:
    file_path = os.path.join(folder_path, csv)
    try:
        # Try reading the file using default UTF-8 encoding
        df = pd.read_csv(file_path)
        df_list.append(df)
    except UnicodeDecodeError:
        try:
            # If UTF-8 fails, try reading the file using UTF-16 encoding with tab separator
            df = pd.read_csv(file_path, sep='\t', encoding='utf-16')
            df_list.append(df)
        except Exception as e:
            print(f"Could not read file {csv} because of error: {e}")
    except Exception as e:
        print(f"Could not read file {csv} because of error: {e}")

# Concatenate all data into one DataFrame
big_df = pd.concat(df_list, ignore_index=True)

# Save the final result to a new CSV file
big_df.to_csv(os.path.join(folder_path, '/syblack/Downloads/combined_file.csv'), index=False)