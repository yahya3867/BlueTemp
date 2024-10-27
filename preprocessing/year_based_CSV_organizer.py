import os
import shutil

# Set the path to the folder containing your CSV files
source_folder = r'C:\Users\ymasr\OneDrive\Desktop\Code\gcoos_platform_water_temperature_csvs'
# Set the path to where you want the organized folders to be created (can be the same as source_folder)
destination_folder = r"C:\Users\ymasr\OneDrive\Desktop\yearr"

# Ensure the destination folder exists
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

# Loop through each file in the source folder
for filename in os.listdir(source_folder):
    # Check if the file is a CSV file and if it contains a year between 2011 and 2024
    if filename.endswith('.csv'):
        # Extract the year from the filename if it appears in YYYY format
        for year in range(1995, 2025):
            if str(year) in filename:
                # Create a folder for the year if it doesn't already exist
                year_folder = os.path.join(destination_folder, str(year))
                if not os.path.exists(year_folder):
                    os.makedirs(year_folder)
                
                # Move the file into the appropriate year folder
                source_path = os.path.join(source_folder, filename)
                destination_path = os.path.join(year_folder, filename)
                shutil.move(source_path, destination_path)
                print(f"Moved {filename} to {year_folder}")
                break  # Move to the next file after finding the year

print("Files have been organized by year.")
