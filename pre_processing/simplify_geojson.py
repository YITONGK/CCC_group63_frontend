"""
Author: Yitong Kong
"""

import json

big_polygons = ['MOIRA', 'MORNINGTON PENINSULA', 'SOUTHERN GRAMPIANS', 'MILDURA', 'GOLDEN PLAINS', 'SWAN HILL',
                'GLENELG', 'CAMPASPE', 'GANNAWARRA', 'GREATER GEELONG', 'WELLINGTON', 'EAST GIPPSLAND', 'LATROBE',
                'INDIGO', 'COLAC OTWAY', 'CORANGAMITE', 'MOYNE', 'TOWONG', 'MANSFIELD']


def cut_down(polygon):
    while len(polygon) > 10000:
        polygon = [point for index, point in enumerate(polygon) if (index % 2 != 0)]
    return polygon


with open('../data/0.99_output_geo.json', 'r', encoding='utf-8') as file:
    localities = json.load(file)
    for lga in localities:
        if lga['LGA_NAME'] in big_polygons:
            simplified_polygon = cut_down(lga["coordinates"])
            lga["coordinates"] = simplified_polygon
    with open('../data/simplified_0.99_output_geo.json', 'w', encoding='utf-8') as f:
        json.dump(localities, f)
