import json
from elasticsearch8 import Elasticsearch, helpers
import os


def get_absolute_path(file_name):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    abs_file_path = os.path.join(dir_path, file_name)
    return abs_file_path


def main():
    client = Elasticsearch(
        "https://elasticsearch-master.elastic.svc.cluster.local:9200",
        verify_certs=False,
        basic_auth=("elastic", "elastic"),
    )
    count = 0
    file_path = get_absolute_path("output_geo.json")
    with open(file_path, "r", encoding="utf-8") as f:
        geo_data = json.load(f)

    for lga_data in geo_data:
        lga_name = lga_data['LGA_NAME']
        coordinates = lga_data['coordinates']
        nested_coordinates = [{"lat": coordinate[0], "lon": coordinate[1]} for coordinate in coordinates]

        action = {
            "_index": "geoinfo",
            "_source": {
                "LGA_NAME": lga_name,
                "coordinates": nested_coordinates
            }
        }
        helpers.bulk(client, action)
        count += 1

    return json.dumps(
        {"status": 200, "message": "Successfully inserted records: " + str(count)}
    )



















# curl -XPUT -k 'https://127.0.0.1:9200/geoinfo' \
#    --user 'elastic:elastic' \
#    --header 'Content-Type: application/json' \
#    --data '{
#   "settings": {
#     "index": {
#       "number_of_shards": 3,
#       "number_of_replicas": 1
#     }
#   },
#   "mappings": {
#     "properties": {
#       "LGA_NAME": {
#         "type": "keyword"
#       },
#       "coordinates": {
#         "type": "nested",
#         "properties": {
#           "lat": {
#             "type": "double"
#           },
#           "lon": {
#             "type": "double"
#           }
#         }
#       }
#     }
#   }
# }' | jq '.'
