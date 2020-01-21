### General Python ###

## os

# current path
import os
folder_path = os.path.dirname(os.path.abspath(__file__))

### Web Scraping ###

## Beautiful Soup ##

# Basic usage
from bs4 import BeautifulSoup
soup = BeautifulSoup(html_doc, 'html.parser')

print(soup.prettify())

for link in soup.find_all('a'):
    print(link.get('href'))

