from io import StringIO
import logging
import json
import requests
import csv
from flask import current_app


def main():
    # assert year.isnumeric()
    # assert month.isnumeric()
    # URL for the CSV file
    url = "https://reg.bom.gov.au/climate/dwo/202403/text/IDCJDW3050.202403.csv"

    # Send HTTP request
    response = requests.get(url)
    current_app.logger.info(f"Harvested one weather observation")

    # Check if the request was successful
    if response.status_code == 200:
        # Read the content into memory from the response
        content = StringIO(response.text)

        # Initialize the CSV reader, skipping the first 7 lines of metadata
        reader = csv.reader(content)
        for _ in range(8):
            next(reader)

        # Read and clean headers
        headers = next(reader)[1:]  # Skip the first empty item
        headers = [
            header.strip() for header in headers if header
        ]  # Clean headers from empty spaces and remove blanks
        # print("Headers:", headers)  # Debug print to confirm headers

        records = []

        # Read each row in the CSV file, skipping the first empty item in each row
        for row in reader:
            if row:  # Ensure row is not empty
                cleaned_row = row[1:]  # Skip the first empty item
                if len(cleaned_row) == len(
                    headers
                ):  # Ensure row data aligns with headers
                    record = dict(zip(headers, cleaned_row))
                    records.append(record)
                else:
                    print(
                        "Mismatched row:", cleaned_row
                    )  # Debug print to check any mismatched row

        # Convert the list of dictionaries to a JSON string
        json_data = json.dumps(records)
        # print(json_data)
        requests.post(
            url="http://router.fission/addobservations",
            headers={"Content-Type": "application/json"},
            data=json.dumps(json_data),
        )

        return json_data
    else:
        # Return error message if the request failed
        return f"Failed to retrieve data: {response.status_code}"


# Running the function for testing
if __name__ == "__main__":
    main()
    # get_weather_data("2024", "03")
