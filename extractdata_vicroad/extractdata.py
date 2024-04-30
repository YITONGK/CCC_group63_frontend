# import os
# import io
# import requests
# import pandas as pd
#
# def extract_data(url):
#     response = requests.get(url)
#     if response.status_code == 200:
#         # Read CSV data using pandas
#         data = pd.read_csv(io.StringIO(response.text))
#         # Convert the DataFrame to JSON format
#         json_data = data.to_json(orient='records')
#         # Print the converted JSON data
#         return json_data
#     else:
#         print("Failed to fetch data, status code:", response.status_code)
#
# def main():
#     # Get URL from environment variable
#     #url = os.getenv('URL1')
#     url = 'https://vicroadsopendatastorehouse.vicroads.vic.gov.au/opendata/Road_Safety/ACCIDENT.csv'
#     # Extract data
#     return extract_data(url)
#
import os
import io
import csv
import json
import requests

# def extract_data(url):
#     response = requests.get(url)
#     if response.status_code == 200:
#         # Use csv.reader to parse the CSV data from the response
#         reader = csv.DictReader(io.StringIO(response.text))
#
#         # Convert the CSV data to JSON by reading it into a list of dicts
#         json_data = json.dumps(list(reader), indent=4)  # Use indent for pretty-printing
#
#         # Return or print the JSON data
#         return json_data
#     else:
#         print("Failed to fetch data, status code:", response.status_code)
#
# def main():
#     # Get URL from environment variable
#     url = 'https://vicroadsopendatastorehouse.vicroads.vic.gov.au/opendata/Road_Safety/ATMOSPHERIC_COND.csv'
#     # Extract data and print
#     return extract_data(url)
#
# # if __name__ == "__main__":
# #     main()
import os
import io
import csv
import json
import requests


# def extract_data(url):
#     response = requests.get(url)
#     if response.status_code == 200:
#         # Use csv.reader to parse the CSV data from the response
#         reader = csv.DictReader(io.StringIO(response.text))
#
#         # Convert the CSV data to JSON by reading it into a list of dicts
#         json_data = json.dumps(list(reader), indent=4)  # Use indent for pretty-printing
#
#         # Return or print the JSON data
#         print(json_data)
#         return json_data
#     else:
#         print("Failed to fetch data, status code:", response.status_code)
#
#
# def main():
#     # Get URL from environment variable
#     url = 'https://vicroadsopendatastorehouse.vicroads.vic.gov.au/opendata/Road_Safety/ACCIDENT.csv'
#     # Extract data and print
#     return extract_data(url)


import os
import io
import csv
import json
import requests

def extract_data(url):
    # 使用 stream=True 开启流式传输
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        # 创建一个 StringIO 对象来逐步写入数据
        buffer = io.StringIO()

        # 逐块读取数据，这里的 chunk_size 可以根据需要调整
        for chunk in response.iter_content(chunk_size=1024):
            # 将二进制数据转换为文本后写入 buffer
            buffer.write(chunk.decode('utf-8'))

        # 将 buffer 的指针移回开始位置，准备读取
        buffer.seek(0)

        # 使用 csv.DictReader 从 StringIO 对象中读取 CSV 数据
        reader = csv.DictReader(buffer)

        # 转换 CSV 数据为 JSON 格式
        json_data = json.dumps(list(reader), indent=4)  # 使用 indent 美化 JSON 输出

        # 打印或返回 JSON 数据

        return json_data
    else:
        print("Failed to fetch data, status code:", response.status_code)

def main():
    # Get URL from environment variable or hardcode for demonstration
    url = 'https://vicroadsopendatastorehouse.vicroads.vic.gov.au/opendata/Road_Safety/ACCIDENT.csv'
    # Extract data and print
    return extract_data(url)


