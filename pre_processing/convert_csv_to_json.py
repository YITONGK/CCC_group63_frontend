import csv
import json

csv_file_path = "data/weather.csv"
json_file_path = "data/upload_weather.json"

# Read the CSV and add data to a dictionary
data = []
with open(csv_file_path, newline="", encoding="utf-8") as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for row in csv_reader:
        data.append(row)

# Write the data to a JSON file
with open(json_file_path, "w", encoding="utf-8") as jsonfile:
    json.dump(data, jsonfile, indent=4)

print(f"CSV data successfully converted to JSON and saved to {json_file_path}")
