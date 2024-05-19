"""
Author: Kexin Chen & Zhihao Wang
"""

import logging, json, requests
from elasticsearch8 import Elasticsearch, helpers
from flask import request
from datetime import datetime

client = Elasticsearch(
    "https://elasticsearch-master.elastic.svc.cluster.local:9200",
    verify_certs=False,
    basic_auth=("elastic", "elastic"),
)


def process_accident_locations(records):
    actions = []
    for obs in records:
        action = {
            "_index": "accident_locations",
            "_id": obs["ACCIDENT_NO"],
            "_op_type": "index",
            "_source": obs,
        }
        actions.append(action)

    return actions


def process_roadcondition(records):
    actions = []
    for obs in records:
        action = {
            "_index": "roadcondition",
            "_id": obs["ACCIDENT_NO"],
            "_op_type": "index",
            "_source": obs,
        }
        actions.append(action)

    return actions


def process_weather(records):
    actions = []
    for obs in records:
        date = datetime.strptime(obs["Date"], "%Y-%m-%d").strftime("%Y%m%d")
        obs["Date"] = date

        action = {
            "_index": "weather",
            "_id": date,
            "_op_type": "index",
            "_source": obs,
        }
        actions.append(action)
    return actions


def process_population(records):
    actions = []
    for obs in records:
        action = {
            "_index": "population",
            "_id": obs["lga_name17"],
            "_source": {
                "LGA_NAME": obs["lga_name17"],
                "persons_num": obs["persons_num"],
            },
        }
        actions.append(action)
    return actions


def process_geoinfo(records):
    actions = []
    for obs in records:
        nested_coordinates = [
            {"lat": float(coord[0]), "lon": float(coord[1])}
            for coord in obs["coordinates"]
        ]
        action = {
            "_index": "geoinfo",
            "_source": {"LGA_NAME": obs["LGA_NAME"], "coordinates": nested_coordinates},
        }
        actions.append(action)
    return actions


def get_index_name_and_validate():
    index_name = request.headers["X-Fission-Params-Indexname"]
    if index_name == "accidents" or index_name == "weather":
        url = "http://router.fission.svc.cluster.local/extract/" + index_name
        response = requests.get(url, verify=False)
        data = json.loads(response.text)["message"]
    elif index_name == "weather2022":
        index_name = "weather"
        data = process_weather(request.get_json())
    elif index_name == "accident_locations":
        data = process_accident_locations(request.get_json())
    elif index_name == "geoinfo":
        data = process_geoinfo(request.get_json())
    elif index_name == "population":
        data = process_population(request.get_json())
    elif index_name == "roadcondition":
        data = process_roadcondition(request.get_json())
    else:
        data = []
    return index_name, data


def upload_data(index_name, actions):
    try:
        # Perform bulk indexing
        # actions = process_roadcondition(records)
        # if index_name == "weather":
        helpers.bulk(client, actions)
        # return
        return True, f"Successfully uploaded data to {index_name}"
    except Exception as e:
        logging.error(f"Failed to upload data to Elasticsearch: {str(e)}")
        return False, str(e)


def main():
    try:
        index_name, data = get_index_name_and_validate()
        if data is None:
            return json.dumps({"message": f"Error: {index_name}"})

        # upload_data(index_name, data)
        # return json.dumps(
        #     {"status": 200, "message": f"Successfully uploaded data to {index_name}"}
        # )
        success, message = upload_data(index_name, data)
        if success:
            return json.dumps({"status": 200, "message": message})
        else:
            return json.dumps({"status": 500, "message": message})
    except Exception as e:
        return json.dumps({"message": f"Error: {e}"})


if __name__ == "__main__":
    print(main())
