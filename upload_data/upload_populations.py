import json
import requests

with open("../data/population.json", "r") as f:
    records = json.load(f)

print(records[0])
actions = []
for obs in records:
    action = {
        "_index": "population",
        "_id": obs["lga_name17"],
        "_source": {"LGA_NAME": obs["lga_name17"], "persons_num": obs["persons_num"]},
    }
    actions.append(action)

url = "http://127.0.0.1:9090/put/population"
response = requests.put(url, json=actions)

print("Status Code:", response.status_code)
print("Response Body:", response.text)


# curl -XGET -k "https://127.0.0.1:9200/geoinfo/_search"\
#   --header 'Content-Type: application/json'\
#   --data '{
#     "query": {
#         "match": {
#             "LGA_NAME": "MERRI-BEK"
#         }
#       }
#   }'\
#   --user 'elastic:elastic' | jq '.'
