"""Web Scraping"""

from bs4 import BeautifulSoup

## Beautiful Soup ##

# Basic usage
html_doc = "<html><body>Hi!</body></html>"
soup = BeautifulSoup(html_doc, 'html.parser')

print(soup.prettify())

for link in soup.find_all('a'):
    print(link.get('href'))
