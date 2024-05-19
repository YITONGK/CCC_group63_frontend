"""
Author: Yitong Kong & Kexin Chen
"""

import csv
import requests
from datetime import datetime


def get_weather_data():
    file_path = "data/weather.csv"
    try:
        with open(file_path, "r") as file:
            reader = csv.DictReader(file)
            next(reader)
            return [row for row in reader]
    except FileNotFoundError as e:
        print("ERROR: ", e)
        return None


records = get_weather_data()
print(records[0])
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

url = "http://127.0.0.1:9090/put/weather2022"
response = requests.put(url, json=actions)

print("Status Code:", response.status_code)
print("Response Body:", response.text)
