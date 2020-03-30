"""Using the project URLs downloaded from ./download_project_urls.py, downloads
the html webpage for each project and saves them all to a folder.
Warning: This will download ~3 GB of data, be prepared!
"""

import os
import requests
import progressbar  # install with `pip install progressbar2`

URLS_FILE_PATH = os.path.dirname(os.path.abspath(__file__))
URLS_FILE_PATH = os.path.join(
    URLS_FILE_PATH, r'Data\Projects URLs\WB Projects Urls.txt')

DATA_FOLDER_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER_PATH = os.path.join(DATA_FOLDER_PATH, 'Data')
DATA_FOLDER_PATH = os.path.join(DATA_FOLDER_PATH, 'Projects HTML')
if not os.path.exists(DATA_FOLDER_PATH):
    os.makedirs(DATA_FOLDER_PATH)


def main():
    # open downloaded urls
    urls = []
    with open(URLS_FILE_PATH, 'r') as urls_file:
        urls = urls_file.readlines()
    urls = [url.strip('\n') for url in urls]

    already_downloaded = os.listdir(DATA_FOLDER_PATH)

    for url in progressbar.progressbar(urls):
        project_id = url.split('/')[-1]
        if project_id + '.html' in already_downloaded:
            continue
        data = requests.get(url)
        with open(DATA_FOLDER_PATH + '\\' + project_id + '.html', 'wb') as output_file:
            output_file.write(data.content)

    print(f'Succesfully downloaded {len(urls)} files.')


if __name__ == "__main__":
    main()
