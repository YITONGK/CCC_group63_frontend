import csv
import json
import os.path
from elasticsearch8 import Elasticsearch, helpers


def get_absolut_path(file_name):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    abs_file_path = os.path.join(dir_path, file_name)
    return abs_file_path


def get_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            datalist = []
            csv_dict = csv.DictReader(f)
            for row in csv_dict:
                row['LATITUDE'] = float(row['LATITUDE'])
                row['LONGITUDE'] = float(row['LONGITUDE'])
                datalist.append(row)
        # output = json.dumps(datalist, indent=4)
        # print(output)
        return datalist
    except FileNotFoundError as e:
        print("error: ", e)
        return None
    except ValueError as e:
        print("Error in converting LATITUDE or LONGITUDE to float: ", e)
        return None


def main():
    client = Elasticsearch(
        "https://elasticsearch-master.elastic.svc.cluster.local:9200",
        verify_certs=False,
        basic_auth=("elastic", "elastic"),
    )
    count = 0
    records = get_data(get_absolut_path("accident_location.csv"))

    if records is None:
        return json.dumps({"status_code": 500, "message": "File not found"})

    actions = []

    for obs in records:
        action = {
            "_index": "accident_locations",
            "_id": obs['ACCIDENT_NO'],
            "_op_type": "index",
            "_source": obs,
        }
        actions.append(action)
        if len(actions) == 500:
            helpers.bulk(client, actions)
            actions = []

    if actions:
        helpers.bulk(client, actions)

    return json.dumps(
        {"status_code": 200, "message": f"Successfully added {count} records"}
    )


if __name__ == '__main__':
    main()
