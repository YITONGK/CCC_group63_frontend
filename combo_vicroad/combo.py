import os
import io
import csv
import json
import requests
from flask import current_app, request
from elasticsearch8 import Elasticsearch

def extract_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        # Use csv.reader to parse the CSV data from the response
        reader = csv.DictReader(io.StringIO(response.text))

        # Convert the CSV data to JSON by reading it into a list of dicts
        json_data = json.dumps(list(reader))  # Use indent for pretty-printing

        # Return or print the JSON data
        return json_data
    else:
        print("Failed to fetch data, status code:", response.status_code)

def main():
    url = 'https://vicroadsopendatastorehouse.vicroads.vic.gov.au/opendata/Road_Safety/ACCIDENT.csv'
    # Extract data and print
    data = extract_data(url)

    client = Elasticsearch (
        'https://elasticsearch-master.elastic.svc.cluster.local:9200',
        verify_certs=False,
        basic_auth=('elastic', 'elastic')
    )
    json_data = json.loads(data)
    for obs in json_data:
        print("here")
        res = client.index(
            #index = index_name,
            index='accidents',
            id=obs.get("ACCIDENT_NO"),
            body=obs
        )
        current_app.logger.info(f'Indexed observation {obs["ACCIDENT_NO"]}')

    return 'ok'

