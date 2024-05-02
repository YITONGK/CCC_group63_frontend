import csv
import json
import os

def get_absolute_path(file_name):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    abs_file_path = os.path.join(dir_path, file_name)
    return abs_file_path

def read_first_five_rows(file_path):
    with open(file_path, newline='') as file:
        reader = csv.reader(file)
        next(reader)
        return [next(reader) for _ in range(5)]

def main():

    file_path = get_absolute_path('accident_road_surface.csv')
    try:
        data = read_first_five_rows(file_path)
        json_data = json.dumps(data)
        return json_data
    except FileNotFoundError:
        return json.dumps({"error": "File not found"})
    except Exception as e:
        return json.dumps({"error": str(e)})


