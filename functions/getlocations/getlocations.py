import csv
import json
import os
import requests
from io import StringIO
from elasticsearch8 import Elasticsearch, helpers


def get_absolute_path(file_name):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    abs_file_path = os.path.join(dir_path, file_name)
    return abs_file_path


def read_all_rows(file_path):
    with open(file_path, newline="") as file:
        reader = csv.DictReader(file)
        next(reader)
        return [row for row in reader]


def main():
    # return json.dumps(
    #     {"status": 200, "message": "Successfully inserted records" }
    # )
    # file_path = get_absolute_path("accident_location.csv")
    file_path = "https://fae230b4ae01.ngrok.app/location_with_name.csv"

    client = Elasticsearch(
        "https://elasticsearch-master.elastic.svc.cluster.local:9200",
        verify_certs=False,
        basic_auth=("elastic", "elastic"),
    )
    actions = []
    count = 0
    # records = read_all_rows(file_path)
    try:
        response = requests.get(file_path, verify=False)
        csv_file = StringIO(response.text)
        records = csv.reader(csv_file)
        next(records)
        for obs in records:
            action = {
                "_index": "accident_locations",
                "_id": obs[0],
                "_op_type": "index",
                # "_source": {
                #     key: obs[key] for key in obs
                # }
                "_source": {
                    "ACCIDENT_NO": obs[0],
                    "LATITUDE": float(obs[1]),
                    "LONGITUDE": float(obs[2]),
                    "LOCATION": obs[3]
                },
            }
            # print(action)
            # break
            actions.append(action)
            count += 1
            if len(actions) == 500:
                helpers.bulk(client, actions)
                actions = []

        if actions:
            helpers.bulk(client, actions)
    except Exception as e:
        return json.dumps(
            {"status": 500, "message": "failed " + str(e)}
        )

    return json.dumps(
        {"status": 200, "message": "Successfully inserted records: " + str(count)}
    )


# curl -XPUT -k 'https://127.0.0.1:9200/accident_locations' \
#    --user 'elastic:elastic' \
#    --header 'Content-Type: application/json' \
#    --data '{
#   "settings": {
#     "index": {
#             "number_of_shards": 3,
#             "number_of_replicas": 1
#         }
#   },
#   "mappings": {
#     "properties": {
#       "ACCIDENT_NO": {
#         "type": "keyword"
#       },
#       "LATITUDE": {
#         "type": "float"
#       },
#       "LONGITUDE": {
#         "type": "float"
#       },
#       "LOCATION": {
#         "type": "text"
#       }
#     }
#   }
# }'  | jq '.'

main()