import os
import pandas as pd

# Path to the main folder containing each sensor folder with CSV files
sensor_folder_path = '/sensordata
# Create a new folder to save the combined data files
output_folder = '/combined_sensordata"

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Loop through each sensor folder
for sensor_folder in os.listdir(sensor_folder_path):
    sensor_path = os.path.join(sensor_folder_path, sensor_folder)
    if os.path.isdir(sensor_path):  # Check if it's a directory

        # List to hold dataframes for each month's CSV
        sensor_data = []

        # Loop through each CSV file within the sensor folder
        for filename in os.listdir(sensor_path):
            if filename.endswith('.csv'):
                file_path = os.path.join(sensor_path, filename)
                
                # Read the CSV and append to the list
                df = pd.read_csv(file_path)
                sensor_data.append(df)

        # Concatenate all monthly data into a single DataFrame
        if sensor_data:
            combined_df = pd.concat(sensor_data, ignore_index=True)
            
            # Ensure data is sorted by date
            combined_df.sort_values(by='date', inplace=True)
            
            # Define the output path and save the combined data for this sensor
            output_file_path = os.path.join(output_folder, f"{sensor_folder}_combined.csv")
            combined_df.to_csv(output_file_path, index=False)
            print(f"Combined data for {sensor_folder} saved to {output_file_path}")

print("All sensor data has been combined into continuous time series files.")
