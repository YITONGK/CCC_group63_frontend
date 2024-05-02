import json
import requests
from elasticsearch8 import Elasticsearch, helpers


def main():
    client = Elasticsearch(
        "https://elasticsearch-master.elastic.svc.cluster.local:9200",
        verify_certs=False,
        basic_auth=("elastic", "elastic"),
    )
    count = 0
    url = 'https://119a-128-250-28-162.ngrok-free.app/insert_accident_location/accident_location.json'
    response = requests.get(url)
    records = response.json()

    if records is None:
        return json.dumps({"status_code": 500, "message": "File not found"})
    actions = []

    for obs in records:
        action = {
            "_index": "accident_locations",
            "_id": obs['ACCIDENT_NO'],
            "_op_type": "index",
            "_source": obs,
        }
        actions.append(action)
        if len(actions) == 500:
            helpers.bulk(client, actions)
            actions = []
            count += 500

    if actions:
        helpers.bulk(client, actions)
        count += len(actions)

    return json.dumps(
        {"status_code": 200, "message": f"Successfully added {count} records"}
    )

def test():
    url = 'https://119a-128-250-28-162.ngrok-free.app/insert_accident_location/accident_location.json'
    response = requests.get(url)

    if response.status_code == 200:
        try:
            data = response.json()
            print("JSON data retrieved successfully:")
            print(json.dumps(data, indent=4))
            return json.dumps(data, indent=4)
        except json.JSONDecodeError:
            print("Error decoding JSON")
    else:
        return json.dumps({"status_code": 500, "message": "File not found"})
        print("Failed to retrieve file, status code:", response.status_code)


if __name__ == '__main__':
    main()
