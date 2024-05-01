import logging, json, requests, csv
from io import StringIO
from elasticsearch8 import Elasticsearch
import os


def get_weather_data(year, month):
    formatted_date = f"{year}{month:02d}"
    url = f"https://reg.bom.gov.au/climate/dwo/{formatted_date}/text/IDCJDW3050.{formatted_date}.csv"

    # Send HTTP request
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code != 200:
        return json.dumps({"state": "500", "message": "Failed to retrieve data"})

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
            if len(cleaned_row) == len(headers):  # Ensure row data aligns with headers
                record = dict(zip(headers, cleaned_row))

                # Remove unnecessary features
                record.pop("3pm wind direction", None)
                record.pop("9am wind direction", None)
                record.pop("Direction of maximum wind gust", None)

                # Convert data type
                speed = record["9am wind speed (km/h)"]
                record["9am wind speed (km/h)"] = int(speed) if speed != "Calm" else 0
                speed = record["3pm wind speed (km/h)"]
                record["3pm wind speed (km/h)"] = int(speed) if speed != "Calm" else 0

                records.append(record)
            else:
                print(
                    "Mismatched row:", cleaned_row
                )  # Debug print to check any mismatched row

    with open(f"filtered_data_{year}_{month}.json", "w") as f:
        f.write(json.dumps(records))
    return records


def get_absolute_path(file_name):
    # Get the absolute path of the current script
    dir_path = os.path.dirname(os.path.realpath(__file__))

    # Combine the directory path with the filename to get the absolute path
    abs_file_path = os.path.join(dir_path, file_name)

    return abs_file_path


def get_weather_json():
    # Print current working directory to understand where the function is running
    # cwd = os.getcwd()
    # print("Current working directory: " + cwd)

    # Specify the path to the file relative to the current working directory if needed
    # file_path = os.path.join(cwd, "storeweather/filtered_data_2023_3.json")

    file_path = get_absolute_path("filtered_data_2023_3.json")
    # file_path = "filtered_data_2023_3.json"
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError as e:
        print("ERROR: ", e)
        return None


def main():
    # client = Elasticsearch(
    #     "https://elasticsearch-master.elastic.svc.cluster.local:9200",
    #     verify_certs=False,
    #     basic_auth=("elastic", "elastic"),
    # )
    count = 0
    records = get_weather_json()

    if records is None:
        return json.dumps({"status_code": 500, "message": "File not found"})

    for obs in records:
        try:
            # res = client.index(index="weather", id=f'{obs["Date"]}', body=obs)
            count += 1
            logging.info("A new observation has been added.")
        except Exception as e:
            print(f"Failed to add observation, {e}")
            continue
            # return json.dumps({"status_code": 400, "text": f"Failed to add observation, {e}"})

    return json.dumps(
        {"status_code": 200, "message": f"Successfully added {count} records"}
    )


if __name__ == "__main__":
    main()
