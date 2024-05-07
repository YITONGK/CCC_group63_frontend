import json

big_polygons = []
with open('../../data/0.99_output_geo.json', 'r', encoding='utf-8') as f:
    d = json.load(f)
    for lga in d:
        # if lga["LGA_NAME"] == "MOIRA":
        # print(lga["LGA_NAME"], len(lga["coordinates"]))
        if len(lga['coordinates']) > 10000:
            big_polygons.append(lga["LGA_NAME"])
    print(big_polygons)
