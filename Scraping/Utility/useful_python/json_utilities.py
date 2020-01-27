"""JSON"""
import json

# Pretty print Python Dict to JSON file
OUTPUT_FILE = "data.json"
DATA_DICT = {'4': 5, '6': 7}

with open(OUTPUT_FILE, 'w') as file:
    file.write(json.dumps(DATA_DICT, sort_keys=True, indent=4))
