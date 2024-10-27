import os
import pandas as pd

# Path to the folder containing all your combined CSV files
source_folder = '/combined_sensordata'

# Loop through each CSV file in the source folder
for filename in os.listdir(source_folder):
    if filename.endswith('.csv'):
        file_path = os.path.join(source_folder, filename)
        
        # Read the CSV file
        df = pd.read_csv(file_path)
        
        # Convert the 'date' column to datetime format, using the specific format string
        df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%dT%H:%M:%SZ', errors='coerce')
        
        # Drop rows with NaT in the 'date' column if any parsing issues occurred
        df.dropna(subset=['date'], inplace=True)
        
        # Save the file back to the same location
        df.to_csv(file_path, index=False)
        print(f"Converted 'date' column to datetime format in {filename}")

print("All date columns in the source folder have been converted to datetime format.")
