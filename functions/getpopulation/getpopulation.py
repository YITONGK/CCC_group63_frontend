import json
from elasticsearch8 import Elasticsearch, helpers
import os


def get_absolute_path(file_name):
    # Get the absolute path of the current script
    dir_path = os.path.dirname(os.path.realpath(__file__))

    # Combine the directory path with the filename to get the absolute path
    abs_file_path = os.path.join(dir_path, file_name)

    return abs_file_path


def main():
    client = Elasticsearch(
        "https://elasticsearch-master.elastic.svc.cluster.local:9200",
        verify_certs=False,
        basic_auth=("elastic", "elastic"),
    )
    file_path = get_absolute_path("population.json")
    # file_path = "population.json"
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    actions = []
    for entry in data:
        action = {
            "_index": "population",
            "_source": {
                "LGA_NAME": entry['lga_name17'],
                "persons_num": entry['persons_num']
            }
        }
        actions.append(action)
    if actions:
        try:
            helpers.bulk(client, actions)
            return json.dumps({"status": 200, "message": f"success adding {len(actions)} lga population"})
        except Exception as e:
            return json.dumps({"status": 500, "message": str(e)})


if __name__ == "__main__":
    main()


# curl -XPUT -k 'https://127.0.0.1:9200/population' \
#    --user 'elastic:elastic' \
#    --header 'Content-Type: application/json' \
#    --data '{
#   "settings": {
#     "index": {
#             "number_of_shards": 3,
#             "number_of_replicas": 1
#         }
#   },
#   "mappings": {
#     "properties": {
#       "LGA_NAME": {
#         "type": "keyword"
#       },
#       "persons_num": {
#         "type": "integer"
#       }
#     }
#   }
# }'  | jq '.'


# with open("../../data/0.99_output_geo.json", "r", encoding="utf-8") as f:
#     data = json.load(f)
# lga_geo = []
# for entry in data:
#     lga_geo.append(entry['LGA_NAME'])
#
# print("population lga: ", len(lga_pop))
# print("geoinfo lga: ", len(lga_geo))
# print(lga_pop)
# print("-------------------")
# print(lga_geo)
# for lga in lga_pop:
#     if lga not in lga_geo:
#         print(lga)
# print("---------------------------------------------------------")
# for lga in lga_geo:
#     if lga not in lga_pop:
#         print(lga)
# print(lga_pop)
# print(lga_geo)