import json
import requests
# from elasticsearch8 import Elasticsearch

# client = Elasticsearch(
#     "https://elasticsearch-master.elastic.svc.cluster.local:9200",
#     verify_certs=False,
#     basic_auth=("elastic", "elastic"),
# )


# def post_record_to_es(record):
#     # Post the record to Elasticsearch
#     try:
#         response = client.index(
#             index="accidents", id=f'{record['ACCIDENT_NO']}', body=record
#         )
#         return {"status": 200, "message": f"Success: {response}"}
#     except Exception as e:
#         return {"status": 400, "message": f"Failed to add observation, {e}"}


def extract_data(url):
    # 使用 stream=True 开启流式传输
    try:
        response = requests.get(url, stream=True)
    except Exception as e:
        print("Request failed:", e)
        return {"status": 500, "message": "Internal server error"}

    if response.status_code == 200:
        if response.encoding is None:
            response.encoding = "utf-8-sig"

        header = []
        num = 0
        for line in response.iter_lines(decode_unicode=True):
            num += 1
            if header == []:
                header = line.split(",")
            else:
                record = dict(zip(header, line.split(",")))
                # res = post_record_to_es(record)
                # if res["status"] == 400:
                #     return res
                # print(record)
            if num == 5:
                break
        return {"status": 200, "message": "OK"}
    else:
        print("Failed to fetch data, status code:", response.status_code)
        return {"status": 500, "message": "Failed to fetch the csv file"}


# def process_csv_stream(url):
#     # Send a GET request and stream the response
#     with requests.get(url, stream=True) as response:
#         if response.status_code != 200:
#             return {"status": 500, "message": "Failed to fetch the csv file"}

#         # Wrap the line stream with StringIO so csv can read it
#         line_stream = (line.decode("utf-8") for line in response.iter_lines())
#         reader = csv.DictReader(line_stream)

#         # Process each row as it's read, without storing the entire file in memory
#         for record in reader:
#             print(record)
#             res = post_record_to_es(record)
#             if res["status"] == 400:
#                 return res
#     return {"status": 200, "message": "OK"}


def main():
    # Get URL from environment variable or hardcode for demonstration
    url = "https://vicroadsopendatastorehouse.vicroads.vic.gov.au/opendata/Road_Safety/ACCIDENT.csv"
    # Extract data and print
    return json.dumps({"status": 200, "message": "Fetched files were successfully"})
    # return json.dumps(extract_data(url))
    # return json.dumps(process_csv_stream(url))


if __name__ == "__main__":
    main()
