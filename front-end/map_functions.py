import folium

# 全地图显示函数
def display_all_map(processed_data):
    # 创建地图实例
    all_map = folium.Map(location=[-36.5, 144.5], zoom_start=7, tiles='CartoDB positron')

    # 遍历地理数据并添加到地图
    for item in processed_data['geo_data']:
        lga_name = item['LGA_NAME']
        coordinates = item['coordinates']
        persons_number = processed_data['population_lookup'].get(lga_name, "No data available")
        accident_count = processed_data['accident_counts'].get(lga_name, 0)

        popup_content = f"<strong>LGA Name:</strong> {lga_name}<br>" + \
                        f"<strong>Population:</strong> {persons_number}<br>" + \
                        f"<strong>Accident Count:</strong> {accident_count}"

        folium.Polygon(
            locations=[(coord['lat'], coord['lon']) for coord in coordinates],
            color='blue',
            fill=True,
            fill_color='cyan',
            tooltip=lga_name,
            popup=folium.Popup(popup_content, max_width=300),
            weight=2
        ).add_to(all_map)

    return all_map

# 城市地图显示函数
def display_city_map(processed_data, city_name):
    """
    Display a map for a specific city (LGA) with population and accident data.
    
    :param processed_data: Dictionary containing geo_data, population_lookup, and accident_counts.
    :param city_name: The name of the city to display on the map.
    :return: Folium Map object if city is found, otherwise None.
    """
    # 提取数据
    geo_data = processed_data['geo_data']
    population_lookup = processed_data['population_lookup']
    accident_counts = processed_data['accident_counts']

    # 标准化输入的城市名称
    city_name = city_name.strip().upper()
    
    # 搜索指定的城市，并显示相关信息
    found = False
    
    for item in geo_data:
        if item['LGA_NAME'].strip().upper() == city_name:
            found = True
            coordinates = item['coordinates']
            lga_name = item['LGA_NAME']

            # 计算坐标的平均位置以设置地图中心
            latitudes, longitudes = zip(*[(coord['lat'], coord['lon']) for coord in coordinates])
            average_lat = sum(latitudes) / len(latitudes)
            average_lon = sum(longitudes) / len(longitudes)

            # 创建地图实例 - 显示指定城市
            city_map = folium.Map(location=[average_lat, average_lon], zoom_start=10, tiles='CartoDB positron')

            # 从人口查找表中获取人口信息
            persons_number = population_lookup.get(lga_name, "No data available")

            # 从车祸统计数据中获取车祸数量
            accident_count = accident_counts.get(lga_name, 0)
            
            popup_content = f"<strong>LGA Name:</strong> {lga_name}<br>" + \
                            f"<strong>Population:</strong> {persons_number}<br>" + \
                            f"<strong>Accident Count:</strong> {accident_count}"

            # 添加多边形和标记到地图
            folium.Polygon(
                locations=[(coord['lat'], coord['lon']) for coord in coordinates],
                color='blue',
                fill=True,
                fill_color='pink',
                tooltip=lga_name,
                popup=folium.Popup(popup_content, max_width=300)
            ).add_to(city_map)

            return city_map

    if not found:
        print("The specified city name was not found.")
        return None
    

def display_map_with_accidents_severity_dot(processed_data):
    # 创建地图实例
    all_map = folium.Map(location=[-36.5, 144.5], zoom_start=7, tiles='CartoDB positron')

    # 遍历地理数据并添加到地图
    for item in processed_data['geo_data']:
        lga_name = item['LGA_NAME']
        coordinates = item['coordinates']

        folium.Polygon(
            locations=[(coord['lat'], coord['lon']) for coord in coordinates],
            color='blue',
            fill=True,
            fill_color='cyan',
            tooltip=lga_name,
            weight=2
        ).add_to(all_map)
    
    # Function to choose marker color based on severity
    def choose_color(severity):
        if severity == '1':
            return 'red'  # Fatal accident
        elif severity == '2':
            return 'orange'  # Serious injury accident
        elif severity == '3':
            return 'yellow'  # Other injury accident
        else:
            return 'green'  # Non injury accident

    # Plotting accidents with circle markers
    for accident in processed_data['accident_details']:
        severity = accident['severity']
        location = (accident['latitude'], accident['longitude'])
        
        folium.CircleMarker(
            location=location,
            radius=5,  # Increase radius for visibility
            color=choose_color(severity),
            fill=True,
            fill_color=choose_color(severity),
            fill_opacity=0.7
        ).add_to(all_map)

    return all_map
