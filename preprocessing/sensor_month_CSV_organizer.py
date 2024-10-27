import os
import shutil

# Base directory path where the 'year' folder is located
base_dir = 'year'  # Adjust this path to your actual 'year' folder location

# Function to organize files by sensor and month within each yearly folder
def organize_files(base_dir):
    # Loop through each year folder in the base directory
    for year_folder in os.listdir(base_dir):
        year_path = os.path.join(base_dir, year_folder)
        
        # Check if the item is a folder and named as a year (numeric check)
        if os.path.isdir(year_path) and year_folder.isdigit():
            # Process each file in the yearly folder
            for file_name in os.listdir(year_path):
                # Ensure we're only processing CSV files
                if file_name.endswith('.csv'):
                    # Extract sensor name and month from the file name
                    try:
                        # Extract sensor name between 'station-' and '_YYYY'
                        sensor_start = file_name.index('station-') + len('station-')
                        sensor_end = file_name.index('_', sensor_start)
                        sensor_name = file_name[sensor_start:sensor_end]
                        
                        # Extract month between 'YYYY_' and '_sea'
                        month_start = file_name.index('_', sensor_end) + 1
                        month_end = file_name.index('_sea', month_start)
                        month = file_name[month_start:month_end]
                        
                        # Define the destination folder path
                        sensor_folder_path = os.path.join(year_path, sensor_name, month)
                        
                        # Create the sensor/month folder if it doesn't exist
                        os.makedirs(sensor_folder_path, exist_ok=True)
                        
                        # Move the file to the appropriate sensor/month folder
                        src_file = os.path.join(year_path, file_name)
                        dst_file = os.path.join(sensor_folder_path, file_name)
                        shutil.move(src_file, dst_file)
                    
                    except ValueError:
                        print(f"Skipping file due to unexpected format: {file_name}")

# Call the function to organize the files
organize_files(base_dir)
