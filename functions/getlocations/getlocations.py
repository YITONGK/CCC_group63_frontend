import csv
import json
import os
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
    file_path = get_absolute_path("accident_location.csv")
    client = Elasticsearch(
        "https://elasticsearch-master.elastic.svc.cluster.local:9200",
        verify_certs=False,
        basic_auth=("elastic", "elastic"),
    )
    actions = []
    count = 0
    records = read_all_rows(file_path)
    for obs in records:
        # print(obs)

        action = {
            "_index": "accident_locations",
            "_id": obs["ACCIDENT_NO"],
            "_op_type": "index",
            # "_source": {
            #     key: obs[key] for key in obs
            # }
            "_source": obs,
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

    return json.dumps(
        {"status": 200, "message": "Successfully inserted records: " + str(count)}
    )
