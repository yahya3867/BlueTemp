import requests
from bs4 import BeautifulSoup
import os

# Base URL of the main directory
base_url = "https://data.gcoos.org/data/waf/csv_by_observation/"

# Directory to save downloaded files
os.makedirs("gcoos_water_temperature_csvs", exist_ok=True)

# Function to get all subdirectories for each year
def get_year_directories():
    response = requests.get(base_url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, "html.parser")
    year_links = [base_url + link.get("href") for link in soup.find_all("a") if link.get("href").endswith("/")]
    print("Year directories found:", year_links)  # Debugging statement
    return year_links

# Loop through each year directory
for year_url in get_year_directories():
    print(f"Checking directory: {year_url}")  # Debugging statement
    
    # Fetch the page content of the year directory
    response = requests.get(year_url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Search for files ending with water_temperature.csv
    file_found = False  # Track if file is found in each directory
    for link in soup.find_all("a"):
        file_name = link.get("href")
        if file_name.endswith("water_temperature.csv"):
            file_url = year_url + file_name
            file_path = os.path.join("gcoos_water_temperature_csvs", f"{year_url.split('/')[-2]}_{file_name}")
            
            # Download and save the file
            csv_data = requests.get(file_url, headers={"User-Agent": "Mozilla/5.0"})
            with open(file_path, "wb") as f:
                f.write(csv_data.content)
                
            print(f"Downloaded {file_path}")
            file_found = True
    
    if not file_found:
        print(f"No water_temperature.csv files found in {year_url}")

print("Download process complete.")
