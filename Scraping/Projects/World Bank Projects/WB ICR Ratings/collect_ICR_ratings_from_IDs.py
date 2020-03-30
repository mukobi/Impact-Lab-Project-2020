"""Using the project URLs downloaded from ./download_project_urls.py, downloads
the html webpage for each project and saves them all to a folder.
Warning: This will download ~3 GB of data, be prepared!
"""

import os
import requests
import json
import progressbar  # install with `pip install progressbar2`

# periodically write to file every n requests
REQUESTS_PER_FILE_WRITE_INTERVAL = 100

# define which fields we care about saving
FIELDS_TO_SAVE = [
    'outcome',  # Outcome Rating
    'evaluation_riskdo',  # Risk To Development Outcome
    'bankqualityatentry',  # NOTE: Hidden on WB project webpage
    'bankqualityofsupervision',  # NOTE: Hidden on WB project webpage
    'overallbankperf',  # Bank Performance
    'overallborrowperf',  # Borrower Performance
    # NOTE: field doesn't appear to match, but is what's used on the WB project webpage
    'borrowcompliance',  # Government Performance
    # NOTE: field doesn't appear to match, but is what's used on the WB project webpage
    'borrowimplementation',  # Implementing Agency
    'icrquality',  # Icr Quality
    'mequality',  # M&E Quality
]


# configure file IO
IDS_FILE_PATH = os.path.dirname(os.path.abspath(__file__))
IDS_FILE_PATH = os.path.join(
    IDS_FILE_PATH, r'Data\Projects IDs\WB Projects IDs.txt')

OUTPUT_FILE_PATH = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE_PATH = os.path.join(OUTPUT_FILE_PATH, 'Data')
OUTPUT_FILE_PATH = os.path.join(OUTPUT_FILE_PATH, 'Projects ICR Ratings')
if not os.path.exists(OUTPUT_FILE_PATH):
    os.makedirs(OUTPUT_FILE_PATH)
OUTPUT_FILE_PATH = os.path.join(OUTPUT_FILE_PATH, 'ICR_Ratings.json')


def main():
    """Main execution."""

    # open downloaded IDs
    ids = []
    with open(IDS_FILE_PATH, 'r') as urls_file:
        ids = urls_file.readlines()
    ids = [url.strip('\n') for url in ids]

    # import already downloaded ratings
    all_ratings = {}
    if os.path.exists(OUTPUT_FILE_PATH):
        with (open(OUTPUT_FILE_PATH)) as file:
            all_ratings = json.loads(file.read())

    # download ratings

    for i, project_id in enumerate(progressbar.progressbar(ids)):
        if project_id in all_ratings.keys():
            continue  # already downloaded this project's ratings

        url = f'https://search.worldbank.org/api/v2/projects?format=json&fl=*&id={project_id}&apilang=en'

        data = requests.get(url)
        data = json.loads(data.content)

        project_data = data['projects'][project_id]

        project_ratings = {}
        for field in FIELDS_TO_SAVE:
            try:
                project_ratings[field] = project_data[field][0]
            except KeyError:
                project_ratings[field] = "missing"

        all_ratings[project_id] = project_ratings

        if (i + 1) % REQUESTS_PER_FILE_WRITE_INTERVAL == 0:
            write_json_to_file(all_ratings, OUTPUT_FILE_PATH)

    print(f'Succesfully downloaded {len(ids)} files.')


def write_json_to_file(data, filepath):
    """Writes the json-serializable `data` to file with path `filepath`."""
    with open(filepath, 'w') as file:
        file.write(json.dumps(data))


if __name__ == "__main__":
    main()
