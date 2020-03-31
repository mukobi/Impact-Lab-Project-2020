"""Using the project ratings downloaded from ./collect_ICR_ratings_from_IDs.py
(which were downloaded in JSON format) and converts them into a CSV file.
"""
import os
import csv
import json

INPUT_FILENAME = 'ICR_Ratings.json'
assert INPUT_FILENAME[-5:] == '.json'
OUTPUT_FILENAME = 'ICR_Ratings.csv'
assert OUTPUT_FILENAME[-4:] == '.csv'

ICR_RATINGS_FOLDER = os.path.dirname(os.path.abspath(__file__))
ICR_RATINGS_FOLDER = os.path.join(
    ICR_RATINGS_FOLDER, r'Data/Projects ICR Ratings')  # assumes this folder exists

INPUT_FILEPATH = os.path.join(ICR_RATINGS_FOLDER, INPUT_FILENAME)
OUTPUT_FILEPATH = os.path.join(ICR_RATINGS_FOLDER, OUTPUT_FILENAME)


def main():
    """Main execution function."""
    # Import downloaded ratings
    json_ratings = {}
    with (open(INPUT_FILEPATH)) as file:
        json_ratings = json.loads(file.read())
    print(f'Read data from {len(json_ratings.keys())} projects.')

    # Generate header
    headers = ['project_id']
    source_element = json_ratings[list(json_ratings.keys())[0]]
    for rating_type in source_element.keys():
        headers += [rating_type + '_' + rating_key
                    for rating_key in source_element[rating_type].keys()]

    with open(OUTPUT_FILEPATH, mode='w', newline='\n') as csv_file:
        csv_writer = csv.writer(
            csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(headers)
        for project_id in json_ratings.keys():
            row = [project_id]
            for rating_type in json_ratings[project_id]:
                row += [rating
                        for rating in json_ratings[project_id][rating_type].values()]
            csv_writer.writerow(row)

    print(f'Successfully wrote {len(json_ratings.keys())} rows.')


if __name__ == "__main__":
    main()
