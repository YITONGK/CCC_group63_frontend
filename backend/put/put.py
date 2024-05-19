"""
Author: Kexin Chen & Zhihao Wang
"""

import logging, json, requests
from elasticsearch8 import Elasticsearch, helpers
from flask import request

client = Elasticsearch(
    "https://elasticsearch-master.elastic.svc.cluster.local:9200",
    verify_certs=False,
    basic_auth=("elastic", "elastic"),
)


def get_index_name_and_validate():
    index_name = request.headers["X-Fission-Params-Indexname"]
    if index_name == "accidents" or index_name == "weather":
        url = "http://router.fission.svc.cluster.local/extract/" + index_name
        response = requests.get(url, verify=False)
        data = json.loads(response.text)["message"]
    elif index_name == "weather2022":
        index_name = "weather"
    else:
        data = request.get_json()
    return index_name, data


def upload_data(index_name, actions):
    # try:
    # Perform bulk indexing
    helpers.bulk(client, actions)
    # return
    # return True, f"Successfully uploaded data to {index_name}"
    # except Exception as e:
    #     logging.error(f"Failed to upload data to Elasticsearch: {str(e)}")
    #     return False, str(e)


def main():
    try:
        index_name, data = get_index_name_and_validate()
        if data is None:
            return json.dumps({"message": f"Error: {index_name}"})

        upload_data(index_name, data)
        return json.dumps(
            {"status": 200, "message": f"Successfully uploaded data to {index_name}"}
        )
        # success, message = upload_data(index_name, data)
        # if success:
        # return json.dumps({"status": 200, "message": message})
        # else:
        #     return json.dumps({"status": 500, "message": message})
    except Exception as e:
        return json.dumps({"message": f"Error: {e}"})


if __name__ == "__main__":
    print(main())
