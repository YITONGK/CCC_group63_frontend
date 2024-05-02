import logging, json, requests, csv
from io import StringIO
from elasticsearch8 import Elasticsearch
import os

def get_absolute_path(file_name):
    # Get the absolute path of the current script
    dir_path = os.path.dirname(os.path.realpath(__file__))

    # Combine the directory path with the filename to get the absolute path
    abs_file_path = os.path.join(dir_path, file_name)

    return abs_file_path


def get_weather_json():
    # Print current working directory to understand where the function is running
    # cwd = os.getcwd()
    # print("Current working directory: " + cwd)

    # Specify the path to the file relative to the current working directory if needed
    # file_path = os.path.join(cwd, "storeweather/filtered_data_2023_3.json")

    file_path = get_absolute_path("filtered_data_2023_3.json")
    # file_path = "filtered_data_2023_3.json"
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError as e:
        print("ERROR: ", e)
        return None


def main():
    # client = Elasticsearch(
    #     "https://elasticsearch-master.elastic.svc.cluster.local:9200",
    #     verify_certs=False,
    #     basic_auth=("elastic", "elastic"),
    # )
    count = 0
    records = get_weather_json()

    if records is None:
        return json.dumps({"status_code": 500, "message": "File not found"})

    for obs in records:
        try:
            # res = client.index(index="weather", id=f'{obs["Date"]}', body=obs)
            count += 1
            logging.info("A new observation has been added.")
        except Exception as e:
            print(f"Failed to add observation, {e}")
            continue
            # return json.dumps({"status_code": 400, "text": f"Failed to add observation, {e}"})

    return json.dumps(
        {"status_code": 200, "message": f"Successfully added {count} records"}
    )


if __name__ == "__main__":
    main()
