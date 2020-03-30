"""os utilities"""
import os
import json

# current path
folder_path = os.path.dirname(os.path.abspath(__file__))

# create folder if doesn't exist
OUTPUT_FILE = "sub/folder/data.txt"

if not os.path.exists(os.path.dirname(OUTPUT_FILE)):
    os.makedirs(os.path.dirname(OUTPUT_FILE))

# Write json data to file


def write_json_to_file(data, filepath):
    """Writes the json-serializable `data` to file with path `filepath`."""
    with open(filepath, 'w') as file:
        file.write(json.dumps(data))
