import csv
import json
import os
from elasticsearch8 import Elasticsearch, helpers

#
# def get_absolute_path(file_name):
#     dir_path = os.path.dirname(os.path.realpath(__file__))
#     abs_file_path = os.path.join(dir_path, file_name)
#     return abs_file_path
#
#
# def read_all_rows(file_path):
#     with open(file_path, newline='') as file:
#         reader = csv.DictReader(file)
#         return [row for row in reader]


def main():
    # try:
    #     file_path = get_absolute_path('accident_road_surface.csv')
    # except Exception as e:
    #     return json.dumps({"status": 500, "message": "get path failure "})
    #
    # try:
    #
    #     client = Elasticsearch(
    #         "https://elasticsearch-master.elastic.svc.cluster.local:9200",
    #         verify_certs=False,
    #         basic_auth=("elastic", "elastic"),
    #     )
    # except Exception as e:
    #     return json.dumps({"status": 500, "message": "es connection failure "})
    #
    # actions = []
    #count = 0
    #
    # try:
    #     records = read_all_rows(file_path)
    # except Exception as e:
    #     return json.dumps({"status": 500, "message": "read file failure "})
    #
    # try:
    #     for obs in records:
    #         action = {
    #             "_index": "roadcondition",
    #             "_id": obs["ACCIDENT_NO"],
    #             "_op_type": "index",
    #             "_source": obs,
    #         }
    #         actions.append(action)
    #         count += 1
    #         if len(actions) == 500:
    #             helpers.bulk(client, actions)
    #             actions = []
    # except Exception as e:
    #     return json.dumps({"status": 500, "message": "insertion failure "})
    #
    # if actions:
    #     helpers.bulk(client, actions)

    return json.dumps(
        {"status": 200, "message": "Successfully inserted records: " + str(0)}
    )