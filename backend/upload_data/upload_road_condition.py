"""
Author: Yitong Kong
"""
import csv
import requests

records = []
with open("../../data/accident_road_surface.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        records.append(row)

actions = []
for obs in records:
    action = {
        "_index": "roadcondition",
        "_id": obs["ACCIDENT_NO"],
        "_source": {"ACCIDENT_NO": obs["ACCIDENT_NO"],
                    "SURFACE_COND": int(obs["SURFACE_COND"]),
                    "SURFACE_COND_DESC": obs["SURFACE_COND_DESC"],
                    "SURFACE_COND_SEQ": int(obs["SURFACE_COND_SEQ"])}
    }
    actions.append(action)

url = "http://127.0.0.1:9090/put/roadcondition"
response = requests.put(url, json=actions)

print("Status Code:", response.status_code)
print("Response Body:", response.text)
