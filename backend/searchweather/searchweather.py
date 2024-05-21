"""
Author: Kexin Chen
"""

import logging, json
from elasticsearch8 import Elasticsearch
from string import Template
import traceback
from flask import request

query_template = Template("""{
    "query": {
        "range": {
            "Date": {
                "gte": "${start_date}",
                "lte": "${end_date}",
                "format": "yyyyMMdd"
            }
        }
    }
}""")


def config(k):
    with open(f"/configs/default/shared-data/{k}", "r") as f:
        return f.read()


def main():
    try:
        if request.method != "GET":
            return json.dumps(
                {"status": 400, "message": "The method is not supported. "}
            )
        start_date = request.headers["X-Fission-Params-Startdate"]
        end_date = request.headers["X-Fission-Params-Enddate"]
    except KeyError as e:
        return {"status": 400, "message": f"Missing date parameter: {str(e)}"}

    # start_date = "20230301"
    # end_date = "20230930"

    client = Elasticsearch(
        "https://elasticsearch-master.elastic.svc.cluster.local:9200",
        # "https://127.0.0.1:9200",
        verify_certs=False,
        basic_auth=(config("ES_USERNAME"), config("ES_PASSWORD")),
        # basic_auth=("elastic", "elastic"),
    )

    # query = query_template.substitute(date=date)
    query_string = query_template.substitute(start_date=start_date, end_date=end_date)
    query = json.loads(query_string)
    print(query)

    try:
        # Execute the search query in Elasticsearch
        res = client.search(
            index="weather",
            body=query,
            size=5000,
            # query={"match_all": {}}
        )
        print(len(res["hits"]["hits"]))
        response = {"status": 200, "response": res["hits"]["hits"]}
    except Exception as e:
        logging.error(f"Error executing search: {str(e)}")
        logging.error(traceback.format_exc())
        response = {
            "status": 500,
            "response": f"Failed to search for weather: {str(e)}",
        }

    # Return the results
    return json.dumps(response)


if __name__ == "__main__":
    main()
