import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin

# Base URL of the main directory
base_url = "https://data.gcoos.org/data/waf/csv_by_platform/"

# Directory to save downloaded files
data_dir = "/data-retriever/data/gcoos_platform_water_temperature_csvs" 
os.makedirs(data_dir, exist_ok=True)

# Log file path
log_dir = "/data-retriever/logs/downloaded-files.log"

# Function to read the log file and return downloaded files
def read_downloaded_files():
    if os.path.exists(log_dir):
        with open(log_dir, "r") as log_file:
            return set(log_file.read().strip().splitlines())
    return set()

# Function to log downloaded files
def log_downloaded_file(file_path):
    with open(log_dir, "a") as log_file:
        log_file.write(file_path + "\n")

# Function to get all subdirectories for each year
def get_year_directories():
    response = requests.get(base_url, headers={"User-Agent": "Mozilla/5.0"})
    response.raise_for_status() # Raise an error for bad responses
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
    for link in soup.find_all("a"):
        file_name = link.get("href")
        if "sea_water_temperature" in file_name:
            file_url = urljoin(year_url, file_name)

            # Debugging statement to show the constructed file URL
            print(f"Constructed file URL: {file_url}")
            
            file_path = os.path.join(data_dir, f"{year_url.split('/')[-2]}_{file_name}")
            
            # Check if the file has already been downloaded
            if os.path.exists(file_path):
                print(f"File already downloaded: {file_path}")
                log_downloaded_file(file_path) # Ensure it's logged as downloaded
                continue # Skip download

            # Download and save the file
            try:
                csv_data = requests.get(file_url, headers={"User-Agent": "Mozilla/5.0"})
                csv_data.raise_for_status() # Raise an error for bad responses

                with open(file_path, "wb") as f:
                    f.write(csv_data.content)
                
                print(f"Downloaded {file_path}")
                log_downloaded_file(file_path) # Log the downloaded file
            except requests.exceptions.RequestException as e:
                print(f"Failed to download {file_url}: {e}")

print("Download process complete.")
