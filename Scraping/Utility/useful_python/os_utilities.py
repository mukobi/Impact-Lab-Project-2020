"""os utilities"""
import os

# current path
folder_path = os.path.dirname(os.path.abspath(__file__))

# create folder if doesn't exist
OUTPUT_FILE = "sub/folder/data.txt"

if not os.path.exists(os.path.dirname(OUTPUT_FILE)):
    os.makedirs(os.path.dirname(OUTPUT_FILE))
