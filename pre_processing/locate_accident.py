import json
import pandas as pd
from shapely.geometry import Point, Polygon


accidents = pd.read_csv("accident_location.csv")

with open("../data/output_geo.json", 'r') as f:
    locations = json.load(f)


polygons = []
for item in locations:
    coordinates = item["coordinates"]
    polygon = Polygon(coordinates)
    if not polygon.is_valid:
        polygon = polygon.buffer(0)  # fix polygon
    if polygon.is_valid:
        polygons.append((item["LGA_NAME"], polygon))
    else:
        print(f"still invalid: {item['LGA_NAME']}")
    polygons.append((item["LGA_NAME"], polygon))

accidents["LOCATION"] = "UNKNOWN"

for index, row in accidents.iterrows():
    point = Point(row['LATITUDE'], row['LONGITUDE'])
    for (location_name, polygon) in polygons:
        if polygon.contains(point):
            print(point, location_name)
            accidents.at[index, 'LOCATION'] = location_name
            break

accidents.to_csv("location_with_name.csv", index=False)

for name, poly in polygons:
    if not poly.is_valid:
        print(f"invalid polygon: {name}")


# curl -XPUT -k 'https://127.0.0.1:9200/accident_locations' \
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
#       "ACCIDENT_NO": {
#         "type": "keyword"
#       },
#       "LATITUDE": {
#         "type": "float"
#       },
#       "LONGTITUDE": {
#         "type": "float"
#       },
#       "LOCATION": {
#         "type": "text"
#       }
#     }
#   }
# }' | jq '.'