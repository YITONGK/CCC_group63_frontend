import json
from elasticsearch8 import Elasticsearch, helpers


def get_json_data(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("FileNotFoundError: The file was not found.")
        return None
    except json.JSONDecodeError:
        print("JSONDecodeError: The file is not in a proper JSON format.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def main():
    client = Elasticsearch(
        "https://elasticsearch-master.elastic.svc.cluster.local:9200",
        verify_certs=False,
        basic_auth=("elastic", "elastic"),
    )
    count = 0
    records = get_json_data("/configs/accident_location.json")

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


if __name__ == '__main__':
    main()
