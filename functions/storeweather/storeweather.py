import logging, json, requests, csv
from io import StringIO
from elasticsearch8 import Elasticsearch, helpers
import os


def get_absolute_path(file_name):
    # Get the absolute path of the current script
    dir_path = os.path.dirname(os.path.realpath(__file__))

    # Combine the directory path with the filename to get the absolute path
    abs_file_path = os.path.join(dir_path, file_name)

    return abs_file_path


def get_weather_data():
    # Print current working directory to understand where the function is running
    # cwd = os.getcwd()
    # print("Current working directory: " + cwd)

    # Specify the path to the file relative to the current working directory if needed
    # file_path = os.path.join(cwd, "storeweather/filtered_data_2023_3.json")

    file_path = get_absolute_path("weather.csv")
    # file_path = "filtered_data_2023_3.json"
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
        verify_certs=False,
        basic_auth=("elastic", "elastic"),
    )
    count = 0
    records = get_weather_data()
    actions = []
    for obs in records:
        # print(obs)

        action = {
            "_index": "weather",
            "_id": obs["Date"],
            "_op_type": "index",
            # "_source": {
            #     key: obs[key] for key in obs
            # }
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
        {"status_code": 200, "message": f"Successfully added {count} records"}
    )


if __name__ == "__main__":
    print(main())
