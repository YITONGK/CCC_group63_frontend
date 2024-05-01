import requests
import json

def main():
    url = 'https://discover.data.vic.gov.au/api/3/action/datastore_search'
    resource_id = 'd48aa391-9f43-4c67-bd90-81192ff2e732'
    limit = 100
    offset = 155665
    end_point = 167300
    all_records = []

    while offset <= end_point:
        params = {
            'resource_id': resource_id,
            'limit': limit,
            'offset': offset
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            records = data['result']['records']
            print(records)
            all_records.extend(records)
            if len(records) < limit:
                break
            offset += limit
        else:
            print("Failed to fetch data, status code:", response.status_code)
            break

    json_data = json.dumps(all_records)
    return json_data