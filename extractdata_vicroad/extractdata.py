# import os
# import io
# import requests
# import pandas as pd
#
# def extract_data(url):
#     response = requests.get(url)
#     if response.status_code == 200:
#         # Read CSV data using pandas
#         data = pd.read_csv(io.StringIO(response.text))
#         # Convert the DataFrame to JSON format
#         json_data = data.to_json(orient='records')
#         # Print the converted JSON data
#         return json_data
#     else:
#         print("Failed to fetch data, status code:", response.status_code)
#
# def main():
#     # Get URL from environment variable
#     #url = os.getenv('URL1')
#     url = 'https://vicroadsopendatastorehouse.vicroads.vic.gov.au/opendata/Road_Safety/ACCIDENT.csv'
#     # Extract data
#     return extract_data(url)
#
import os
import io
import csv
import json
import requests

# def extract_data(url):
#     response = requests.get(url)
#     if response.status_code == 200:
#         # Use csv.reader to parse the CSV data from the response
#         reader = csv.DictReader(io.StringIO(response.text))
#
#         # Convert the CSV data to JSON by reading it into a list of dicts
#         json_data = json.dumps(list(reader), indent=4)  # Use indent for pretty-printing
#
#         # Return or print the JSON data
#         return json_data
#     else:
#         print("Failed to fetch data, status code:", response.status_code)
#
# def main():
#     # Get URL from environment variable
#     url = 'https://vicroadsopendatastorehouse.vicroads.vic.gov.au/opendata/Road_Safety/ATMOSPHERIC_COND.csv'
#     # Extract data and print
#     return extract_data(url)
#
# # if __name__ == "__main__":
# #     main()
#import os
#import io
#import csv
# import json
# import requests
#
#
# def main():
#     url = 'https://discover.data.vic.gov.au/api/3/action/datastore_search'
#     params = {
#         'resource_id': 'd48aa391-9f43-4c67-bd90-81192ff2e732',
#     }
#     response = requests.get(url, params=params)
#     if response.status_code == 200:
#         data = response.json()
#         records = data['result']['records']
#         json_data = json.dumps(records)
#         return json_data
#     else:
#         print("Failed to fetch data, status code:", response.status_code)

import requests
import json

def main():
    url = 'https://discover.data.vic.gov.au/api/3/action/datastore_search'
    resource_id = 'd48aa391-9f43-4c67-bd90-81192ff2e732'
    limit = 100
    offset = 155665
    end_point = 167110
    all_records = []

    while offset <= 167110:
        params = {
            'resource_id': resource_id,
            'limit': limit,
            'offset': offset
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            records = data['result']['records']
            all_records.extend(records)
            if len(records) < limit:
                break
            offset += limit
        else:
            print("Failed to fetch data, status code:", response.status_code)
            break

    json_data = json.dumps(all_records)
    return json_data




