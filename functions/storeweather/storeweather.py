import logging, json, requests, csv
from io import StringIO
from elasticsearch8 import Elasticsearch, helpers
import os
from datetime import datetime


def format_date(date_str):
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    formatted_date = date_obj.strftime("%Y%m%d")  # Convert to 'yyyyMMdd'
    return formatted_date


def get_absolute_path(file_name):
    # Get the absolute path of the current script
    dir_path = os.path.dirname(os.path.realpath(__file__))
    abs_file_path = os.path.join(dir_path, file_name)

    return abs_file_path


def get_weather_data():
    file_path = get_absolute_path("weather2023.csv")
    try:
        with open(file_path, newline="") as file:
            reader = csv.DictReader(file)
            next(reader)
            return [row for row in reader]
    except FileNotFoundError as e:
        print("ERROR: ", e)
        return None


def main():
    client = Elasticsearch(
        "https://elasticsearch-master.elastic.svc.cluster.local:9200",
        # "https://127.0.0.1:9200",
        verify_certs=False,
        basic_auth=("elastic", "elastic"),
    )
    count = 0
    records = get_weather_data()
    actions = []
    for obs in records:
        # print(obs)
        date = format_date(obs["Date"])
        obs["Date"] = date

        action = {
            "_index": "weather",
            "_id": date,
            "_op_type": "index",  # Use 'index' to create or replace a document
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
        {
            "status_code": 200,
            "message": f"Successfully added {count} records",
            "count": count,
        }
    )


if __name__ == "__main__":
    print(main())
