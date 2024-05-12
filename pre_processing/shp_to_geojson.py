import geopandas as gpd
# import fiona
# import pyogrio
from pyproj import Transformer
import json


no_pop_list = ['FRENCH-ELIZABETH-SANDSTONE ISLANDS (UNINC)',
                'MOUNT BULLER ALPINE RESORT (UNINC)',
                'MOUNT HOTHAM ALPINE RESORT (UNINC)',
                'FALLS CREEK ALPINE RESORT (UNINC)',
                'MOUNT STIRLING ALPINE RESORT (UNINC)',
                'GABO ISLAND (UNINC)',
                'MOUNT BAW BAW ALPINE RESORT (UNINC)',
                'LAKE MOUNTAIN ALPINE RESORT (UNINC)']


def geojson_to_json():
    gdf = gpd.read_file("../data/0.99_LGA_POLYGON.shp")
    gdf.to_file("../data/0.99_LGA_POLYGON.geojson", driver='GeoJSON')

    with open("../data/0.99_LGA_POLYGON.geojson", "r", encoding="utf-8") as f:
        geo_data = json.load(f)

    print(len(geo_data['features']))
    transformer = Transformer.from_crs("EPSG:7899", "EPSG:4326", always_xy=True)
    geo_dict = []
    for feature in geo_data['features']:
        lga = feature['properties']['LGA_NAME']
        if lga in no_pop_list:
            continue
        polygon = feature['geometry']['coordinates']
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

    with open('../data/0.99_output_geo.json', 'w', encoding='utf-8') as f:
        json.dump(geo_dict, f)


def generate_test_case():
    with open('../data/simplified_0.99_output_geo.json', 'r', encoding='utf-8') as file:
        localities = json.load(file)
        for lga in localities:
            if lga['LGA_NAME'] == 'WELLINGTON':
                mel = {"LGA_NAME": "WELLINGTON", "coordinates": lga["coordinates"]}
            if lga['LGA_NAME'] == 'CORANGAMITE':
                yarra = {"LGA_NAME": "CORANGAMITE", "coordinates": lga["coordinates"]}
        with open('../data/simplified_0.99_comb.json', 'w', encoding='utf-8') as f:
            json.dump([mel, yarra], f)


geojson_to_json()
# generate_test_case()
