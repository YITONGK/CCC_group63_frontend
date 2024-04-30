import logging, json, requests, csv
from io import StringIO
from elasticsearch8 import Elasticsearch


def get_weather_data(year, month):
    formatted_date = f"{year}{month:02d}"
    url = f"https://reg.bom.gov.au/climate/dwo/{formatted_date}/text/IDCJDW3050.{formatted_date}.csv"

    # Send HTTP request
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code != 200:
        return json.dumps({"state": "400", "message": "Failed to retrieve data"})

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
    
    # with open("filtered_data.json", "w") as f:
    #     f.write(json.dumps(records))
    return records 

def main():
    records = get_weather_data(2024, 3)
    # print(records)
    client = Elasticsearch(
        "https://elasticsearch-master.elastic.svc.cluster.local:9200",
        verify_certs=False,
        basic_auth=("elastic", "elastic"),
    )

    count = 0
    for obs in records:
        try:
            res = client.index(index="weather", id=f'{obs["Date"]}', body=obs)
            count += 1
            logging.info("A new observation has been added.")
        except Exception as e:
            print(f"Failed to add observation, {e}")
            continue
            # return json.dumps({"status_code": 400, "text": f"Failed to add observation, {e}"})

    return json.dumps({"status_code": 200, "message": f"Successfully added {count} records"})

if __name__ == "__main__":
    main()

