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

    file_path = get_absolute_path("road_surface.csv")
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
            "_index": "roadcondition",
            "_id": obs["ACCIDENT_NO"],
            "_op_type": "index",
            "_source": obs
        }
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