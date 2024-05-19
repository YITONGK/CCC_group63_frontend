"""
Author: Yitong Kong
"""

import json
import requests

with open("../../data/simplified_0.99_output_geo.json", "r") as f:
    records = json.load(f)

print(len(records))

actions = []
for obs in records:
    nested_coordinates = [
        {"lat": float(coord[0]), "lon": float(coord[1])} for coord in obs["coordinates"]
    ]
    action = {
        "_index": "geoinfo",
        "_id": obs["LGA_NAME"],
        "_source": {"LGA_NAME": obs["LGA_NAME"], "coordinates": nested_coordinates},
    }
    actions.append(action)

url = "http://127.0.0.1:9090/put/geoinfo"
response = requests.put(url, json=actions)

print("Status Code:", response.status_code)
print("Response Body:", response.text)
