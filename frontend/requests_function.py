"""
Author: Pengjiabei Tang, Xiaoyang Peng
"""

import requests
import json

def fetch_and_process_data():
    # URLs definition
    urls = {
        'population': "http://127.0.0.1:9090/search/population",
        'accidents': "http://127.0.0.1:9090/search/accidents",
        'accident_locations': "http://127.0.0.1:9090/search/accident_locations",
        'geoinfo': "http://127.0.0.1:9090/search/geoinfo",
        'roadcondition': "http://127.0.0.1:9090/search/roadcondition"
    }

    # Fetch data from URLs
    data = {key: requests.get(url).json() for key, url in urls.items()}

    # Initialize processed_data with an empty accident_counts
    processed_data = {
        'population_lookup': {},
        'accident_details': [],
        'geo_data': [],
        'accident_counts': {}  # Initialize empty dictionary for accident counts
    }

    # Check if all data are successfully retrieved and have status 200
    if all(d['status'] == 200 for d in data.values()):
        processed_data['population_lookup'] = {item['LGA_NAME']: item['persons_num'] for item in data['population']['response']}
        processed_data['geo_data'] = data['geoinfo']['response']

        # Create a dictionary for road conditions for quick lookup
        road_condition_map = {cond['ACCIDENT_NO']: cond for cond in data['roadcondition']['response']}

        # Create a dictionary for accident locations for quick lookup
        accident_location_map = {acc['ACCIDENT_NO']: acc for acc in data['accident_locations']['response']}

        # Merge accident details with locations and road conditions
        for accident in data['accidents']['response']:
            location = accident_location_map.get(accident['ACCIDENT_NO'])
            road_condition = road_condition_map.get(accident['ACCIDENT_NO'])
            if location and road_condition:
                # Append detailed accident information including latitude, longitude, and road conditions
                processed_data['accident_details'].append({
                    'ACCIDENT_NO': accident['ACCIDENT_NO'],
                    'ACCIDENT_DATE': accident['ACCIDENT_DATE'],
                    'SPEED_ZONE': accident['SPEED_ZONE'],
                    'SEVERITY': accident['SEVERITY'],
                    'LATITUDE': location['LATITUDE'],
                    'LONGITUDE': location['LONGITUDE'],
                    'LOCATION': location['LOCATION'],
                    'SURFACE_COND': road_condition['SURFACE_COND'],
                    'SURFACE_COND_DESC': road_condition['SURFACE_COND_DESC']
                })

        for detail in processed_data['accident_details']:
            lga = detail['LOCATION']
            if lga in processed_data['accident_counts']:
                processed_data['accident_counts'][lga] += 1
            else:
                processed_data['accident_counts'][lga] = 1

        return processed_data
    else:
        return None


def fetch_weather_data(start_date, end_date):
    weather_url = f"http://127.0.0.1:9090/searchweather/{start_date}/{end_date}"
    try:
        response = requests.get(weather_url)
        if response.status_code == 200:
            weather_data = response.json()
            if 'response' in weather_data:
                weather_list = weather_data['response']
                rainfall_data = {item['_source']['Date']: item['_source']['Rainfall (mm)'] for item in weather_list}
                return rainfall_data
            else:
                return {'error': 'Weather data format is incorrect'}
        else:
            return {'error': 'Failed to fetch weather data, status code: {}'.format(response.status_code)}
    except requests.RequestException as e:
        return {'error': 'Failed to fetch weather data, error: {}'.format(str(e))}
    except json.JSONDecodeError as e:
        return {'error': 'JSON decoding failed, error: {}'.format(str(e))}