import geopandas as gpd
# import fiona
# import pyogrio
from pyproj import Transformer
import json

gdf = gpd.read_file("../data/LGA_POLYGON.shp")
gdf.to_file("../data/LGA_POLYGON.geojson", driver='GeoJSON')

with open("../data/LGA_POLYGON.geojson", "r", encoding="utf-8") as f:
    geo_data = json.load(f)

print(len(geo_data['features']))
transformer = Transformer.from_crs("EPSG:7899", "EPSG:4326", always_xy=True)
geo_dict = []
for feature in geo_data['features']:
    lga = feature['properties']['LGA_NAME']
    polygon = feature['geometry']['coordinates']
    # print(type(polygon), type((polygon[0])), type(polygon[0][0]), type(polygon[0][0][0]), type(polygon[0][0][0][0]))
    # print(lga, len(coordinates))
    coordinate_list = []
    for line in polygon:
        for point in line:
            for coordinate in point:
                if type(coordinate) == float:
                    lon, lat = transformer.transform(point[0], point[1])
                    coordinate_list.append([lat, lon])
                else:
                    lon, lat = transformer.transform(coordinate[0], coordinate[1])
                    coordinate_list.append([lat, lon])

    geo_dict.append({"LGA_NAME": lga, "coordinates": coordinate_list})

with open('../data/output_geo.json', 'w', encoding='utf-8') as f:
    json.dump(geo_dict, f)


def generate_test_case():
    with open('../data/output_geo.json', 'r', encoding='utf-8') as file:
        localities = json.load(file)
        for lga in localities:
            if lga['LGA_NAME'] == 'MELBOURNE':
                mel = {"LGA_NAME": "MELBOURNE", "coordinates": lga["coordinates"]}
            if lga['LGA_NAME'] == 'YARRA':
                yarra = {"LGA_NAME": "YARRA", "coordinates": lga["coordinates"]}
        with open('../data/comb.json', 'w', encoding='utf-8') as f:
            json.dump([mel, yarra], f)
