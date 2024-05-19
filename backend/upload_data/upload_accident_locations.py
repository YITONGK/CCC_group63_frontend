"""
Author: Yitong Kong
"""
import csv
import requests

records =[]
with open("../../data/accident_location_name.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        records.append(row)

# print(records[0],type(records[0]["ACCIDENT_NO"]),type(records[0]["LATITUDE"]),type(records[0]["LONGITUDE"]),type(records[0]["LOCATION"]))

actions = []
for obs in records:
    action = {
        "_index": "accident_locations",
        "_id": obs["ACCIDENT_NO"],
        "_source": {"ACCIDENT_NO": obs["ACCIDENT_NO"],
                    "LATITUDE": float(obs["LATITUDE"]),
                    "LONGITUDE": float(obs["LONGITUDE"]),
                    "LOCATION": obs["LOCATION"]}
    }
    actions.append(action)

url = "http://127.0.0.1:9090/put/accident_locations"
response = requests.put(url, json=actions)

print("Status Code:", response.status_code)
print("Response Body:", response.text)
