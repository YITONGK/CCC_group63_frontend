import csv
import datetime


def read_weather(filepath, keyname):
    data = []
    with open(filepath, mode="r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        for row in reader:
            year = row["Year"]
            month = row["Month"]
            day = row["Day"]
            date = f"{year}-{month}-{day}"
            # date = datetime.strptime(f"{year}-{month}-{day}", "%Y-%m-%d")
            # print(accident_date, row['ACCIDENT_TIME'])
            data.append([date, row[keyname]])
    return data


def merge_data(rainfall, maxtemp, mintemp):
    data = []
    for i in range(len(rainfall)):
        data.append([rainfall[i][0], rainfall[i][1], maxtemp[i][1], mintemp[i][1]])
    return data


def write_csv(filepath, data):
    with open(filepath, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "Date",
                "Rainfall (mm)",
                "Maximum temperature (°C)",
                "Minimum temperature (°C)",
            ]
        )
        writer.writerows(data)


rainfall = read_weather("RAINFALL2023.csv", "Rainfall amount (millimetres)")
maxtemp = read_weather("MAXTEMP2023.csv", "Maximum temperature (Degree C)")
mintemp = read_weather("MINTEMP2023.csv", "Minimum temperature (Degree C)")
merged_data = merge_data(rainfall, maxtemp, mintemp)
write_csv("weather2023.csv", merged_data)
