import csv
import json

data = []
with open("../data/location_with_name.csv", 'r') as f:

    csv_reader = csv.DictReader(f)
    for row in csv_reader:
        data.append(row)

with open("../data/location_with_name.json", mode='w', encoding='utf-8') as json_file:
    json.dump(data, json_file, indent=4)
