import json
import requests
from elasticsearch8 import Elasticsearch, helpers
import os
import logging

logging.basicConfig(level=logging.INFO)


# big_polygons = ['MOIRA', 'MORNINGTON PENINSULA', 'SOUTHERN GRAMPIANS', 'MILDURA', 'GOLDEN PLAINS', 'SWAN HILL',
#                 'GLENELG', 'CAMPASPE', 'GANNAWARRA', 'GREATER GEELONG', 'WELLINGTON', 'EAST GIPPSLAND', 'LATROBE',
#                 'INDIGO', 'COLAC OTWAY', 'CORANGAMITE', 'MOYNE', 'TOWONG', 'MANSFIELD']


def main():
    filepath = "https://bb125090596d.ngrok.app/simplified_0.99_output_geo.json"
    client = Elasticsearch(
        "https://elasticsearch-master.elastic.svc.cluster.local:9200",
        verify_certs=False,
        basic_auth=("elastic", "elastic"),
    )
    count = 0
    actions = []
    lga_added = []
    points_added = 0
    try:
        response = requests.get(filepath, verify=False)
        if response.status_code == 200:
            geo_data = response.json()
            for lga_data in geo_data:
                # if lga_data['LGA_NAME'] in big_polygons:
                #     continue
                nested_coordinates = [{"lat": float(coord[0]), "lon": float(coord[1])} for coord in lga_data['coordinates']]
                action = {
                    "_index": "geoinfo",
                    "_source": {
                        "LGA_NAME": lga_data['LGA_NAME'],
                        "coordinates": nested_coordinates
                    }
                }
                actions.append(action)
                count += 1
                helpers.bulk(client, actions)
                lga_added.append(action["_source"]["LGA_NAME"])
                points_added += len(action["_source"]["coordinates"])
                actions = []
            #     if len(actions) == 10:
            #         helpers.bulk(client, actions)
            #         for action in actions:
            #             lga_added.append(action["_source"]["LGA_NAME"])
            #             points_added += len(action["_source"]["coordinates"])
            #         actions = []
            # if actions:
            #     helpers.bulk(client, actions)
            return json.dumps({"status": 200, "message": "success"})
        else:
            logging.error(f"Failed to fetch data: HTTP {response.status_code}")
            return json.dumps({"status": response.status_code, "message": "Failed to fetch data"})
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return json.dumps({"status": 500,
                           "message": str(e),
                           "points added": str(points_added),
                           "lga added": str(len(lga_added)),
                           "failed lga": action["_source"]["LGA_NAME"]})


# if __name__ == "__main__":
#     main()



# def get_absolute_path(file_name):
#     dir_path = os.path.dirname(os.path.realpath(__file__))
#     abs_file_path = os.path.join(dir_path, file_name)
#     return abs_file_path


# def main():
#     client = Elasticsearch(
#         "https://elasticsearch-master.elastic.svc.cluster.local:9200",
#         verify_certs=False,
#         basic_auth=("elastic", "elastic"),
#     )
#     count = 0
#     file_path = get_absolute_path("output_geo.json")
#     with open(file_path, "r", encoding="utf-8") as f:
#         geo_data = json.load(f)
#
#     for lga_data in geo_data:
#         lga_name = lga_data['LGA_NAME']
#         coordinates = lga_data['coordinates']
#         nested_coordinates = [{"lat": coordinate[0], "lon": coordinate[1]} for coordinate in coordinates]
#
#         action = {
#             "_index": "geoinfo",
#             "_source": {
#                 "LGA_NAME": lga_name,
#                 "coordinates": nested_coordinates
#             }
#         }
#         helpers.bulk(client, action)
#         count += 1
#
#     return json.dumps(
#         {"status": 200, "message": "Successfully inserted records: " + str(count)}
#     )

# url = "https://810e-128-250-0-203.ngrok-free.app/output_geo.json"
# try:
#     response = requests.get(url)
#     if response.status_code == 200:
#         print("connection succeed")
#         data = response.json()
#         print(type(data), type(data[0]))
#     else:
#         print("connection error")
# except Exception as e:
#     print(f"An error occurred: {e}")


def validate():
    total_points = 0
    with open('../../data/simplified_0.99_output_geo.json', 'r', encoding='utf-8') as f:
        d = json.load(f)
        for lga in d:
            print(lga["LGA_NAME"], len(lga['coordinates']))
            total_points += len(lga['coordinates'])
        print(len(d))
        print(total_points)


validate()





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
#             "type": "float"
#           },
#           "lon": {
#             "type": "float"
#           }
#         }
#       }
#     }
#   }
# }' | jq '.'
