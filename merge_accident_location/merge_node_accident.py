import csv
from datetime import datetime


def read_accidents(filepath, start_date, end_date):
    accidents = []
    with open(filepath, mode='r', newline='', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            accident_date = datetime.strptime(row['ACCIDENT_DATE'], '%Y-%m-%d')
            if start_date <= accident_date <= end_date:
                # print(accident_date, row['ACCIDENT_TIME'])
                accidents.append(row['ACCIDENT_NO'])
    return accidents


def read_nodes(filepath):
    nodes = {}
    with open(filepath, mode='r', newline='', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            nodes[row['ACCIDENT_NO']] = (row['LATITUDE'], row['LONGITUDE'])
    return nodes


def merge_data(accidents, nodes):
    merged_data = []
    for accident_no in accidents:
        if accident_no in nodes:
            latitude, longitude = nodes[accident_no]
            merged_data.append([accident_no, latitude, longitude])
    return merged_data


def write_csv(filepath, data):
    with open(filepath, mode='w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerow(['ACCIDENT_NO', 'LATITUDE', 'LONGITUDE'])
        writer.writerows(data)


accidents_filtered_2022 = read_accidents('/Users/felikskong/Desktop/CCC_group63_project2/merge_accident_location/ACCIDENT.csv', datetime(2022, 1, 1), datetime(2022, 12, 30))
nodes_data = read_nodes('/Users/felikskong/Desktop/CCC_group63_project2/merge_accident_location/NODE.csv')
merged_results = merge_data(accidents_filtered_2022, nodes_data)
write_csv('location_2022.csv', merged_results)


# def print_csv_headers(filepath):
#     with open(filepath, mode='r', newline='') as file:
#         reader = csv.DictReader(file)
#         print(reader.fieldnames)
