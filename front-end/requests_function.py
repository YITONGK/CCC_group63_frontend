import requests

def fetch_and_process_data():
    # 定义URLs
    urls = {
        'population': "http://127.0.0.1:9090/search/population",
        'accidents': "http://127.0.0.1:9090/search/accidents",
        'accident_locations': "http://127.0.0.1:9090/search/accident_locations",
        'geoinfo': "http://127.0.0.1:9090/search/geoinfo"
    }

    # 发送请求并获取数据
    data = {key: requests.get(url).json() for key, url in urls.items()}

    # 检查所有数据的状态是否为200
    if all(d['status'] == 200 for d in data.values()):
        processed_data = {
            'population_lookup': {item['LGA_NAME']: item['persons_num'] for item in data['population']['response']},
            'accident_counts': {},
            'severities': [],  # 存储所有事故的 SEVERITY
            'geo_data': data['geoinfo']['response']
        }

        # 从事故位置响应中建立事故详细信息
        for item in data['accident_locations']['response']:
            lga_name = item['LOCATION']
            accident_no = item['ACCIDENT_NO']

            # 从事故数据中查找相应的事故详细信息
            accident_info = next((acc for acc in data['accidents']['response'] if acc['ACCIDENT_NO'] == accident_no), None)
            if accident_info:
                # 将 SEVERITY 信息添加到列表
                processed_data['severities'].append(accident_info.get('SEVERITY'))

                # 计数该 LGA 的事故总数
                if lga_name in processed_data['accident_counts']:
                    processed_data['accident_counts'][lga_name] += 1
                else:
                    processed_data['accident_counts'][lga_name] = 1

        return processed_data
    else:
        return None