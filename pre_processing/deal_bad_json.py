import json

json_list = []

with open('../data/accident_road_surface.json', 'r') as file:
    for line in file:
        json_obj = json.loads(line.strip())
        json_list.append(json_obj)

with open('output.json', 'w') as outfile:
    json.dump(json_list, outfile, indent=4)
