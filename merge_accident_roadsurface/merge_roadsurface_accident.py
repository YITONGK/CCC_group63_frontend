import csv
from datetime import datetime

def read_accidents(filepath, start_date, end_date):
    accidents = []
    with open(filepath, mode='r', newline='', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            accident_date = datetime.strptime(row['ACCIDENT_DATE'], '%Y-%m-%d')
            if start_date <= accident_date <= end_date:
                accidents.append(row['ACCIDENT_NO'])
    return accidents

def read_road_surface(filepath):
    road_surface = {}
    with open(filepath, mode='r', newline='', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            road_surface[row['ACCIDENT_NO']] = (row['SURFACE_COND'], row['SURFACE_COND_DESC'], row['SURFACE_COND_SEQ'])
    return road_surface

def merge_data(accidents, road_surface):
    merged_data = []
    for accident_no in accidents:
        if accident_no in road_surface:
            surface_cond, surface_cond_desc, surface_cond_seq = road_surface[accident_no]
            merged_data.append([accident_no, surface_cond, surface_cond_desc, surface_cond_seq])
    return merged_data

def write_csv(filepath, data):
    with open(filepath, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ACCIDENT_NO', 'SURFACE_COND', 'SURFACE_COND_DESC', 'SURFACE_COND_SEQ'])
        writer.writerows(data)

accidents_filtered = read_accidents('ACCIDENT.csv', datetime(2022, 1, 1), datetime(2023, 9, 30))
road_surface_data = read_road_surface('ROAD_SURFACE_COND.csv')
merged_results = merge_data(accidents_filtered, road_surface_data)
write_csv('accident_road_surface.csv', merged_results)
