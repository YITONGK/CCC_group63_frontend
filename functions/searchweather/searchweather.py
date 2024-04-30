import logging, json, requests, csv
from io import StringIO
from flask import current_app, request
from elasticsearch8 import Elasticsearch
from string import Template

query_template = Template('''{
    "query": {
        "match": {
            "Date": "${date}"
        }
    }
}''')

def main():
    
    try:
        date= request.headers['X-Fission-Params-Date']
    except KeyError:
         date= None

    
    client = Elasticsearch(
        "https://elasticsearch-master.elastic.svc.cluster.local:9200",
        verify_certs=False,
        basic_auth=("elastic", "elastic"),
    )

    query = query_template.substitute(date=date)

    # Execute the search query in Elasticsearch
    res = client.search(
        index='weather',  # Make sure this matches the actual index name in your Elasticsearch
        body=json.loads(query)
    )

    # Return the results
    return json.dumps({"status": 200, "response": res})
