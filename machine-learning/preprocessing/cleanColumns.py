import os
import pandas as pd

# Path to the folder containing all your combined CSV files
source_folder = '/combined_sensordata'  # Replace with your actual folder path

# List to log files with missing or misaligned columns
issue_log = []

# Function to clean a single CSV file
def clean_csv(file_path):
    # Read the CSV file
    df = pd.read_csv(file_path)
    issues_found = False
    
    # Check and handle duplicate 'qcFlag' columns
    if 'qcFlag.1' in df.columns:
        # Fill missing values in 'qcFlag' with values from 'qcFlag.1'
        df['qcFlag'].fillna(df['qcFlag.1'], inplace=True)
        # Drop the duplicate column
        df.drop(columns=['qcFlag.1'], inplace=True)
        issues_found = True

    # Ensure values are correctly aligned for 'network' and 'platform'
    # Shift 'owner' values to 'network' if 'network' is missing or has NaN values
    if 'network' in df.columns and 'owner' in df.columns:
        df['network'] = df['network'].combine_first(df['owner'])
        df.drop(columns=['owner'], inplace=True)
    elif 'owner' in df.columns:
        # If 'network' is missing, create it from 'owner'
        df['network'] = df['owner']
        df.drop(columns=['owner'], inplace=True)
        issues_found = True

    # Shift 'sensor' values to 'platform' if 'platform' is missing or has NaN values
    if 'platform' in df.columns and 'sensor' in df.columns:
        df['platform'] = df['platform'].combine_first(df['sensor'])
        df.drop(columns=['sensor'], inplace=True)
    elif 'sensor' in df.columns:
        # If 'platform' is missing, create it from 'sensor'
        df['platform'] = df['sensor']
        df.drop(columns=['sensor'], inplace=True)
        issues_found = True

    # Log file if there were issues found
    if issues_found:
        issue_log.append(file_path)

    # Save the cleaned file
    df.to_csv(file_path, index=False)
    print(f"Cleaned file: {file_path}")

# Loop through each CSV file in the folder and clean it
for filename in os.listdir(source_folder):
    if filename.endswith('.csv'):
        file_path = os.path.join(source_folder, filename)
        clean_csv(file_path)

# Print summary of files with issues
if issue_log:
    print("\nFiles with missing or misaligned columns:")
    for file in issue_log:
        print(file)
else:
    print("No files with issues found.")

print("All files have been cleaned.")
