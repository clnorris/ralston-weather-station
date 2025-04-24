import os
from dotenv import load_dotenv
import requests
from datetime import datetime, timedelta
import time  # Import the time module

# Load environment variables from .env file
load_dotenv()

# Retrieve the URL and station ID from environment variables
url = os.getenv("APRSWORLD_URL")
station_id = os.getenv("STATION_ID")

# Validate that the required environment variables are set
if not url:
    raise ValueError("APRSWORLD_URL is not set in the environment variables")
if not station_id:
    raise ValueError("STATION_ID is not set in the environment variables")


# Define the start and end dates
start_date = datetime(2017, 12, 1)
end_date = datetime(2025, 4, 16)

# Function to generate half-month date ranges
def generate_date_ranges(start, end):
    current = start
    while current < end:
        if current.day == 1:
            # First half of the month: 1st to 16th
            mid_month = current.replace(day=16)
        else:
            # Second half of the month: 16th to 1st of the next month
            if current.month == 12:  # Handle December to January transition
                next_month = current.replace(year=current.year + 1, month=1, day=1)
            else:
                next_month = current.replace(month=current.month + 1, day=1)
            mid_month = next_month

        yield current, min(mid_month, end)
        current = mid_month

# Iterate through the date ranges and make requests
for start, stop in generate_date_ranges(start_date, end_date):
    params = {
        "station_id": station_id,
        "view": f"view_{station_id}",
        "start_date": start.strftime("%Y-%m-%d"),
        "start_date_dp": "1",
        "start_date_year_start": "2000",
        "start_date_year_end": "2025",
        "start_date_fmt": "d-M-Y",
        "start_date_day": start.strftime("%d"),
        "start_date_month": start.strftime("%m"),
        "start_date_year": start.strftime("%Y"),
        "stop_date": stop.strftime("%Y-%m-%d"),
        "stop_date_dp": "1",
        "stop_date_year_start": "2000",
        "stop_date_year_end": "2025",
        "stop_date_fmt": "d-M-Y",
        "stop_date_day": stop.strftime("%d"),
        "stop_date_month": stop.strftime("%m"),
        "stop_date_year": stop.strftime("%Y"),
        "format": "csv"
    }

    response = requests.get(url, params=params)

    if response.ok:
        filename = f"data_{start.strftime('%Y%m%d')}_to_{stop.strftime('%Y%m%d')}.csv"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"Data saved to {filename}")
    else:
        print(f"Failed to retrieve data for {start} to {stop}: {response.status_code}")

    time.sleep(2)  # Add a 2-second delay between requests

