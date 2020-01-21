"""Parses all HTML files in ./Data downloaded using ./browser-commands.js and
all of it (sans the very personal bits) to a JSON file for easy analysis.
"""

import os
from bs4 import BeautifulSoup


def main():
    """Does all that parsing."""

    # Get HTML data
    html_data_path = os.path.dirname(os.path.abspath(__file__))
    html_data_path = os.path.join(html_data_path, 'Data')
    html_data_path = os.path.join(html_data_path, 'IFS-HTML')
    print(f'data_path: {html_data_path}')

    all_officer_data = {}

    for i, html_filename in enumerate(os.listdir(html_data_path)):
        individual_officer_data = {}

        # Read HTML file
        with open(os.path.join(html_data_path, html_filename), 'r') as html_file:
            soup = BeautifulSoup(html_file.read(), 'html.parser')

            # Basic info
            individual_officer_data['Basic Info'] = {
                'Name': soup.find(id='Label1').string,
                'Service': soup.find(id='Label2').string,
                'Cadre/Allotment Year': soup.find(id='Label3').string,
                'Date of Birth': soup.find(id='Label4').string,
                'Gender': soup.find(id='Label5').string,
                'Place of Domicile': soup.find(id='lblDomicile').string,
                'Date of Appoinment': soup.find(id='Label6').string,
                'Recruitment Source': soup.find(id='Label8').string,
                'IFS Cadre': soup.find(id='Label9').string, }

            # Educational Qualifications
            qualifications = soup.find(id='GridView1').find_all('td')
            individual_officer_data['Educational Qualifications'] = {
                'Qualification I': qualifications[0].string.replace(u'\xa0', u'none'),
                'Qualification II': qualifications[1].string.replace(u'\xa0', u'none'),
                'Qualification III': qualifications[2].string.replace(u'\xa0', u'none')}
            print(individual_officer_data['Educational Qualifications'])

            # Posting Details
            individual_officer_data['Posting Details'] = {}
            postings = soup.find(id='GridView2')
            if postings:  # check for Not Available
                postings = postings.find_all('tr')[1:]  # first row is labels

        all_officer_data[html_filename] = individual_officer_data

        if i > 5:
            break


if __name__ == "__main__":
    main()
