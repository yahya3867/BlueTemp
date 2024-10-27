import os
import shutil

# Set the path to the main folder that contains yearly folders
source_folder = 'year'
# Create a new folder which will hold your sensor-based folders. 
destination_folder = '/sensordata'

# Ensure the destination folder exists
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

# Loop through each year folder in the source folder
for year_folder in os.listdir(source_folder):
    year_path = os.path.join(source_folder, year_folder)
    if os.path.isdir(year_path):  # Ensure it's a directory

        # Loop through each sensor folder within the year folder
        for sensor_folder in os.listdir(year_path):
            sensor_path = os.path.join(year_path, sensor_folder)
            if os.path.isdir(sensor_path):  # Ensure it's a directory

                # Create a new folder for each sensor in the destination path
                sensor_destination_folder = os.path.join(destination_folder, sensor_folder)
                os.makedirs(sensor_destination_folder, exist_ok=True)
                
                # Loop through each subfolder (if any) in the sensor folder to get the CSV files
                for subfolder in os.listdir(sensor_path):
                    subfolder_path = os.path.join(sensor_path, subfolder)
                    
                    # If there’s an extra layer of folders, look inside it
                    if os.path.isdir(subfolder_path):
                        for filename in os.listdir(subfolder_path):
                            if filename.endswith('.csv'):
                                source_file_path = os.path.join(subfolder_path, filename)
                                # Build a new filename to avoid overwriting (include the year in the filename)
                                new_filename = f"{year_folder}_{filename}"
                                destination_file_path = os.path.join(sensor_destination_folder, new_filename)
                                
                                # Move the file to the new sensor-based folder
                                shutil.move(source_file_path, destination_file_path)
                                print(f"Moved {filename} from {year_folder}/{sensor_folder} to {sensor_folder} folder")
                    # If there’s no extra layer and the files are directly in the sensor folder
                    elif subfolder.endswith('.csv'):
                        source_file_path = os.path.join(sensor_path, subfolder)
                        new_filename = f"{year_folder}_{subfolder}"
                        destination_file_path = os.path.join(sensor_destination_folder, new_filename)
                        shutil.move(source_file_path, destination_file_path)
                        print(f"Moved {subfolder} from {year_folder}/{sensor_folder} to {sensor_folder} folder")

print("All files have been reorganized by sensor.")
