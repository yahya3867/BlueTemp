# Lightweight Official Python Image
FROM python:3.10-slim

# Set working directory
WORKDIR /data-retriever

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Python script into container
COPY data_retrieval.py .

# Create directory to store downloaded CSVs
RUN mkdir -p /data-retriever/gcoos_platform_water_temperature_csvs

# Command to run script
CMD ["python", "data_retrieval.py"]
