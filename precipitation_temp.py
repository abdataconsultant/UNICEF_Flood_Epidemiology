import requests
import pandas as pd

# Get user input for latitude, longitude, start and end dates
latitude = input("Enter latitude: ")
longitude = input("Enter longitude: ")
start_date = input("Enter start date (YYYY-MM-DD): ")
end_date = input("Enter end date (YYYY-MM-DD): ")

# Construct API endpoint URL with user input
url = f"https://archive-api.open-meteo.com/v1/era5?latitude={latitude}&longitude={longitude}&start_date={start_date}&end_date={end_date}&hourly=temperature_2m,precipitation"

# Send GET request to API endpoint
response = requests.get(url)

# Check if request was successful
if response.status_code == 200:
    # Write API response to file
    with open("weather_data.json", "w") as f:
        f.write(response.text)
    print("Data downloaded successfully!")
else:
    print("Error downloading data.")


# Read JSON data into pandas DataFrame
with open("weather_data.json", "r") as f:
    data = pd.read_json(f)

# Print first five rows of DataFrame
print(data.head())
