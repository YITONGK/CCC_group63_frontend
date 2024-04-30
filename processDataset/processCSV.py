import csv
from datetime import datetime

def filter_accidents_by_year(input_file, output_file, year=2023):
    with open(input_file, mode='r', newline='') as infile, open(output_file, mode='w', newline='') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            accident_date = datetime.strptime(row['ACCIDENT_DATE'], '%Y-%m-%d')
            if accident_date.year == year:
                writer.writerow(row)

# Example usage
filter_accidents_by_year('ACCIDENT.csv', 'ACCIDENT2023.csv')
