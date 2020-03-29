"""Downloads the projects urls for all 19000+ projects from the World Bank
Projects API http://search.worldbank.org/api/v2/projects
"""

import os
import json
import requests
import progressbar  # install with `pip install progressbar2`

OUTPUT_FILENAME = 'WB Projects URLs.txt'

DATA_FOLDER_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER_PATH = os.path.join(DATA_FOLDER_PATH, 'Data')
DATA_FOLDER_PATH = os.path.join(DATA_FOLDER_PATH, 'Projects URLs')
if not os.path.exists(DATA_FOLDER_PATH):
    os.makedirs(DATA_FOLDER_PATH)
OUTPUT_FILE_PATH = os.path.join(DATA_FOLDER_PATH, OUTPUT_FILENAME)

# At the time of writing, there were 19303 projects accessible by the API
NUM_PROJECTS_TO_SEACH_FOR = 20000
NUM_PROJECTS_PER_REQUEST = 100

BASE_PROJECT_URL = 'https://projects.worldbank.org/en/projects-operations/project-detail/'


def main():
    """Main execution function."""
    urls_found = []
    num_requests = int(NUM_PROJECTS_TO_SEACH_FOR / NUM_PROJECTS_PER_REQUEST)
    for i in progressbar.progressbar(range(0, num_requests)):
        offset = i * NUM_PROJECTS_PER_REQUEST
        url = ('http://search.worldbank.org/api/v2/projects?format=json&fl=url'
               + f'&source=IBRD&rows={NUM_PROJECTS_PER_REQUEST}&os={offset}')

        response = requests.get(url)
        data = json.loads(response.content)
        for project_id in data['projects']:
            urls_found.append(BASE_PROJECT_URL + project_id)

    with open(OUTPUT_FILE_PATH, 'w') as file:
        file.writelines('\n'.join(urls_found))

    print(f'Wrote {len(urls_found)} lines.')


if __name__ == "__main__":
    main()
