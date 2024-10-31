import os
import shutil
import pandas as pd
import warnings

# Set the main folder path
main_folder = r'C:\Users\ymasr\OneDrive\Desktop\Code\gcoos_platform_water_temperature_csvs'
issue_log = []  # To log files with issues

# Step 1: Organize files by year
def organize_by_year(folder):
    for filename in os.listdir(folder):
        if filename.endswith('.csv'):
            for year in range(1995, 2025):
                if str(year) in filename:
                    year_folder = os.path.join(folder, str(year))
                    os.makedirs(year_folder, exist_ok=True)
                    shutil.move(os.path.join(folder, filename), os.path.join(year_folder, filename))
                    print(f"Moved {filename} to {year_folder}")
                    break
    print("Files organized by year.")

# Step 2: Organize files by sensor and month within each year folder
def organize_by_sensor_and_month(folder):
    for year_folder in os.listdir(folder):
        year_path = os.path.join(folder, year_folder)
        if os.path.isdir(year_path) and year_folder.isdigit():
            for filename in os.listdir(year_path):
                if filename.endswith('.csv'):
                    try:
                        sensor_name = filename.split('station-')[1].split('_')[0]
                        month = filename.split('_')[1]
                        sensor_folder_path = os.path.join(year_path, sensor_name, month)
                        os.makedirs(sensor_folder_path, exist_ok=True)
                        shutil.move(os.path.join(year_path, filename), os.path.join(sensor_folder_path, filename))
                    except (IndexError, ValueError):
                        print(f"Skipping file due to unexpected format: {filename}")

# Step 3: Combine CSVs for each sensor
def combine_sensor_files(folder):
    for year_folder in os.listdir(folder):
        year_path = os.path.join(folder, year_folder)
        if os.path.isdir(year_path):
            for sensor_folder in os.listdir(year_path):
                sensor_path = os.path.join(year_path, sensor_folder)
                if os.path.isdir(sensor_path):
                    combined_data = []
                    for month_folder in os.listdir(sensor_path):
                        month_path = os.path.join(sensor_path, month_folder)
                        if os.path.isdir(month_path):
                            for filename in os.listdir(month_path):
                                if filename.endswith('.csv'):
                                    df = pd.read_csv(os.path.join(month_path, filename))
                                    combined_data.append(df)
                    if combined_data:
                        combined_df = pd.concat(combined_data, ignore_index=True)
                        combined_df.sort_values(by='date', inplace=True)
                        combined_df.to_csv(os.path.join(sensor_path, f"{sensor_folder}_combined.csv"), index=False)
                        print(f"Combined data for {sensor_folder} in {year_folder}.")

# Step 4: Convert date columns to datetime format
def convert_date_format(folder):
    for root, _, files in os.walk(folder):
        for filename in files:
            if filename.endswith('.csv'):
                file_path = os.path.join(root, filename)
                df = pd.read_csv(file_path)
                df['date'] = pd.to_datetime(df['date'], errors='coerce')
                df.dropna(subset=['date'], inplace=True)
                df.to_csv(file_path, index=False)
                print(f"Converted date format in {filename}")

# Step 5: Clean specific columns
def clean_columns(folder):
    for root, _, files in os.walk(folder):
        for filename in files:
            if filename.endswith('.csv'):
                file_path = os.path.join(root, filename)
                df = pd.read_csv(file_path)
                issues_found = False

                # Check and handle duplicate 'qcFlag' columns
                if 'qcFlag.1' in df.columns:
                    df['qcFlag'].fillna(df['qcFlag.1'], inplace=True)
                    df.drop(columns=['qcFlag.1'], inplace=True)
                    issues_found = True

                # Ensure 'network' and 'platform' columns are correctly aligned
                if 'network' in df.columns and 'owner' in df.columns:
                    df['network'] = df['network'].combine_first(df['owner'])
                    df.drop(columns=['owner'], inplace=True)
                    issues_found = True
                if 'platform' in df.columns and 'sensor' in df.columns:
                    df['platform'] = df['platform'].combine_first(df['sensor'])
                    df.drop(columns=['sensor'], inplace=True)
                    issues_found = True

                if issues_found:
                    issue_log.append(file_path)
                df.to_csv(file_path, index=False)
                print(f"Cleaned file: {file_path}")

    if issue_log:
        print("\nFiles with issues:")
        for file in issue_log:
            print(file)

# Step 6: Clean and filter sea_water_temperature values
def clean_sea_water_temperature(folder):
    for root, _, files in os.walk(folder):
        for filename in files:
            if filename.endswith(".csv"):
                csv_path = os.path.join(root, filename)
                df = pd.read_csv(csv_path)
                if 'sea_water_temperature' in df.columns:
                    df.dropna(subset=['sea_water_temperature'], inplace=True)
                    df = df[(df['sea_water_temperature'] >= 10) & (df['sea_water_temperature'] <= 50)]
                    df.to_csv(csv_path, index=False)
                    print(f"Cleaned sea_water_temperature in {filename}")

# Run all steps
organize_by_year(main_folder)
organize_by_sensor_and_month(main_folder)
combine_sensor_files(main_folder)
convert_date_format(main_folder)
clean_columns(main_folder)
clean_sea_water_temperature(main_folder)

print("All preprocessing steps completed.")
