import folium
from folium.plugins import MarkerCluster

def display_all_map(processed_data):

    all_map = folium.Map(location=[-36.5, 144.5], zoom_start=7, tiles='CartoDB positron')

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


def display_city_map(processed_data, city_name):
    """
    Display a map for a specific city (LGA) with population and accident data.
    
    :param processed_data: Dictionary containing geo_data, population_lookup, and accident_counts.
    :param city_name: The name of the city to display on the map.
    :return: Folium Map object if city is found, otherwise None.
    """

    geo_data = processed_data['geo_data']
    population_lookup = processed_data['population_lookup']
    accident_counts = processed_data['accident_counts']

    city_name = city_name.strip().upper()
    
    found = False
    
    for item in geo_data:
        if item['LGA_NAME'].strip().upper() == city_name:
            found = True
            coordinates = item['coordinates']
            lga_name = item['LGA_NAME']

            latitudes, longitudes = zip(*[(coord['lat'], coord['lon']) for coord in coordinates])
            average_lat = sum(latitudes) / len(latitudes)
            average_lon = sum(longitudes) / len(longitudes)

            city_map = folium.Map(location=[average_lat, average_lon], zoom_start=10, tiles='CartoDB positron')

            persons_number = population_lookup.get(lga_name, "No data available")

            accident_count = accident_counts.get(lga_name, 0)
            
            popup_content = f"<strong>LGA Name:</strong> {lga_name}<br>" + \
                            f"<strong>Population:</strong> {persons_number}<br>" + \
                            f"<strong>Accident Count:</strong> {accident_count}"

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
    


# general map with accident dots function 
def display_map_with_accidents_severity_dot(processed_data):

    all_map = folium.Map(location=[-36.5, 144.5], zoom_start=7, tiles='CartoDB positron')

    for item in processed_data['geo_data']:
        lga_name = item['LGA_NAME']
        coordinates = item['coordinates']

        folium.Polygon(
            locations=[(coord['lat'], coord['lon']) for coord in coordinates],
            color='blue',
            fill=True,
            fill_color='cyan',
            tooltip=lga_name,
            weight=0.5,
        ).add_to(all_map)

    def choose_color(severity):
        if severity == '3':
            return 'yellow'
        elif severity == '2':
            return 'orange'
        elif severity == '1':
            return 'red'
        else:
            return 'green'
    
    for accident in processed_data['accident_details']:
        severity = accident['SEVERITY']
        location = (accident['LATITUDE'], accident['LONGITUDE'])

        folium.CircleMarker(
            location=location,
            radius=1,  
            color=choose_color(severity),  
            fill=True,
            fill_color=choose_color(severity),
            fill_opacity=0.0,
        ).add_to(all_map)


    return all_map


# general map with accident cluster function
def display_map_with_clustering_accidents(processed_data):

    all_map = folium.Map(location=[-36.5, 144.5], zoom_start=7, tiles='CartoDB positron')

    for item in processed_data['geo_data']:
        lga_name = item['LGA_NAME']
        coordinates = item['coordinates']

        folium.Polygon(
            locations=[(coord['lat'], coord['lon']) for coord in coordinates],
            color='blue',
            fill=True,
            fill_color='cyan',
            tooltip=lga_name,
            weight=0.5,
        ).add_to(all_map)

    marker_cluster = MarkerCluster().add_to(all_map)  
 
    for accident in processed_data['accident_details']:
        location = (accident['LATITUDE'], accident['LONGITUDE'])
        
        folium.Marker(
            location=location,
            icon=folium.Icon()
        ).add_to(marker_cluster)

    return all_map 