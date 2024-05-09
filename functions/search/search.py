import json
from elasticsearch8 import Elasticsearch
from flask import current_app, request


def get_index_name_and_query():
    index_name = request.headers["X-Fission-Params-Indexname"]
    query = {
        "query": {"match_all": {}},
    }
    if index_name == "roadcondition":
        query = {
            "query": {"match_all": {}},
            "_source": ["ACCIDENT_NO", "SURFACE_COND", "SURFACE_COND_DESC"],
        }
    elif index_name == "accidents":
        query = {
            "query": {"match_all": {}},
            "_source": ["ACCIDENT_NO", "ACCIDENT_DATE", "SEVERITY", "SPEED_ZONE"],
        }
    return index_name, query


def fetch_all_documents(index_name, query):
    client = Elasticsearch(
        "https://elasticsearch-master.elastic.svc.cluster.local:9200",
        verify_certs=False,
        basic_auth=("elastic", "elastic"),
    )
    page = client.search(index=index_name, scroll="2m", size=5000, body=query)
    sid = page["_scroll_id"]
    documents = []

    while True:
        documents.extend([doc["_source"] for doc in page["hits"]["hits"]])
        page = client.scroll(scroll_id=sid, scroll="2m")
        sid = page["_scroll_id"]
        if not page["hits"]["hits"]:
            break
    return documents


def main():
    try:
        index_name, query = get_index_name_and_query()
        documents = fetch_all_documents(index_name, query)
        response = {"status": 200, "response": documents}
    except Exception as e:
        response = {
            "status": 500,
            "response": f"Failed to search in {index_name}: {str(e)}",
        }

    return json.dumps(response)
