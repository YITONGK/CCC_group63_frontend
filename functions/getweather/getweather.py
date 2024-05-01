import logging, json, requests, csv
from io import StringIO
from elasticsearch import Elasticsearch, helpers

def get_weather_data(year, month):
    formatted_date = f"{year}{month:02d}"
    url = f"https://reg.bom.gov.au/climate/dwo/{formatted_date}/text/IDCJDW3050.{formatted_date}.csv"
    response = requests.get(url)
    
    if response.status_code != 200:
        return []

    content = StringIO(response.text)
    reader = csv.reader(content)
    for _ in range(8):
        next(reader)

    headers = next(reader)[1:]  # Adjust to correctly skip non-header content if needed
    headers = [header.strip() for header in headers if header]

    records = []
    for row in reader:
        if row:
            cleaned_row = row[1:]
            if len(cleaned_row) == len(headers):
                record = dict(zip(headers, cleaned_row))
                record = {k: int(v) if 'wind speed' in k and v != 'Calm' else v for k, v in record.items()}
                records.append({
                    "_index": "weather",
                    "_type": "_doc",
                    "_source": record
                })

    return records

def main():
    client = Elasticsearch(
        "https://elasticsearch-master.elastic.svc.cluster.local:9200",
        verify_certs=False,
        basic_auth=("elastic", "elastic"),
    )

    years = range(2019, 2025)
    months = range(1, 13)
    all_records = []

    for year in years:
        for month in months:
            records = get_weather_data(year, month)
            all_records.extend(records)
            if len(all_records) >= 500:  # Bulk index when reaching 500 records or any preferred batch size
                helpers.bulk(client, all_records)
                all_records = []  # Clear list after bulk indexing

    if all_records:  # Make sure to index any remaining records
        helpers.bulk(client, all_records)

    return json.dumps({"status": "success", "message": "Data indexed successfully"})

if __name__ == "__main__":
    print(main())
