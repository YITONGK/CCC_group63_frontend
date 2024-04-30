import logging, json, requests, csv
from io import StringIO
from flask import current_app, request
from elasticsearch8 import Elasticsearch


def main():
    url = "https://reg.bom.gov.au/climate/dwo/202403/text/IDCJDW3050.202403.csv"

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
                records.append(record)
            else:
                print(
                    "Mismatched row:", cleaned_row
                )  # Debug print to check any mismatched row

    client = Elasticsearch(
        "https://elasticsearch-master.elastic.svc.cluster.local:9200",
        verify_certs=False,
        basic_auth=("elastic", "elastic"),
    )

    for obs in records:
        try:
            res = client.index(index="weather", body=obs)
            logging.info("A new observation has been added.")
        except Exception as e:
            print(f"Failed to add observation, {e}")
            continue
            # return json.dumps({"status_code": 400, "text": f"Failed to add observation, {e}"})

    return json.dumps({"status_code": 200, "text": "OK"})
