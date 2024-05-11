import logging, json, requests, csv
from io import StringIO
from elasticsearch8 import Elasticsearch, helpers
from datetime import datetime


def format_date(date_str):
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    formatted_date = date_obj.strftime("%Y%m%d")  # Convert to 'yyyyMMdd'
    return formatted_date


def get_weather_data(year, month):
    formatted_date = f"{year}{month:02d}"
    url = f"https://reg.bom.gov.au/climate/dwo/{formatted_date}/text/IDCJDW3050.{formatted_date}.csv"

    response = requests.get(url)
    if response.status_code != 200:
        return []

    content = StringIO(response.text)

    # Initialize the CSV reader, skipping the first 7 lines of metadata
    reader = csv.reader(content)
    for _ in range(8):
        next(reader)

    # Read and clean headers
    headers = next(reader)[1:]  # Skip the first empty item
    headers = [header.strip() for header in headers if header]
    # print("Headers:", headers)

    records = []

    # Read each row in the CSV file, skipping the first empty item in each row
    for row in reader:
        if row:
            cleaned_row = row[1:]
            if len(cleaned_row) == len(headers):
                record = dict(zip(headers, cleaned_row))

                # Remove unnecessary features
                record.pop("3pm wind direction", None)
                record.pop("9am wind direction", None)
                record.pop("Direction of maximum wind gust", None)

                # Convert data type
                speed = record["9am wind speed (km/h)"]
                if speed:
                    record["9am wind speed (km/h)"] = (
                        int(speed) if speed != "Calm" else 0
                    )
                speed = record["3pm wind speed (km/h)"]
                if speed:
                    record["3pm wind speed (km/h)"] = (
                        int(speed) if speed != "Calm" else 0
                    )

                formatted_date = format_date(record["Date"])  # Convert the date
                record["Date"] = formatted_date

                records.append(
                    {"_index": "weather", "_id": formatted_date, 
                     "_op_type": "index",  # Use 'index' to create or replace a document
                        "_source": {
                            key: record[key]
                            for key in record
                            if key
                            in [
                                "Date",
                                "Rainfall (mm)",
                                "Maximum temperature (°C)",
                                "Minimum temperature (°C)"
                            ]
                        },}
                )
            else:
                print("Mismatched row:", cleaned_row)

    return records


def main():
    client = Elasticsearch(
        "https://elasticsearch-master.elastic.svc.cluster.local:9200",
        verify_certs=False,
        basic_auth=("elastic", "elastic"),
    )
    years = range(2023, 2025)
    months = range(1, 13)
    count = 0
    all_records = []
    for year in years:
        for month in months:
            records = get_weather_data(year, month)
            count += len(records)
            all_records.extend(records)
            if len(all_records) >= 500:
                helpers.bulk(client, all_records)
                all_records = []

    if all_records:
        helpers.bulk(client, all_records)

    return json.dumps(
        {
            "status_code": 200,
            "message": f"Successfully added {count} records",
            "count": count,
        }
    )


if __name__ == "__main__":
    print(main())
