import logging, json, requests, csv
from io import StringIO
from flask import current_app, request
from elasticsearch8 import Elasticsearch
from string import Template
import traceback
from flask import Flask, request

query_template = Template("""{
    "query": {
        "range": {
            "Date": {
                "gte": "${start_date}",
                "lte": "${end_date}",
                "format": "yyyy-MM-dd"
            }
        }
    }
}""")


def main():
    try:
        start_date = request.headers["X-Fission-Params-Startdate"]
        end_date = request.headers["X-Fission-Params-Enddate"]
    except KeyError as e:
        return {"status": 400, "message": f"Missing date parameter: {str(e)}"}

    client = Elasticsearch(
        "https://elasticsearch-master.elastic.svc.cluster.local:9200",
        verify_certs=False,
        basic_auth=("elastic", "elastic"),
    )

    # query = query_template.substitute(date=date)
    query_string = query_template.substitute(start_date=start_date, end_date=end_date)
    query = json.loads(query_string)
    # print(query)

    try:
        # Execute the search query in Elasticsearch
        res = client.search(
            index="weather",
            body=query,
            # query={"match_all": {}}
        )
        response = {"status": 200, "response": str(res["hits"]["hits"])}
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
