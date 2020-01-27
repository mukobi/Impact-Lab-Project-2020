"""Parses all HTML files in ./Data downloaded using ./browser-commands.js and
all of it (sans the very personal bits) to a JSON file for easy analysis.
"""

import json
import os
from bs4 import BeautifulSoup
import progressbar  # install with `pip install progressbar2`

OUTPUT_FILE = "all_ifs_officers.json"  # file to write to


def main():
    """Does all that parsing."""

    # Get HTML data
    data_folder_path = os.path.dirname(os.path.abspath(__file__))
    data_folder_path = os.path.join(data_folder_path, 'Data')
    html_data_path = os.path.join(data_folder_path, 'IFS-HTML')
    print(f'input data path: {html_data_path}')

    all_officer_data = {}

    for html_filename in progressbar.progressbar(os.listdir(html_data_path)):
        individual_officer_data = {}

        # Read HTML file
        with open(os.path.join(html_data_path, html_filename), 'r', encoding="utf8") as html_file:
            soup = BeautifulSoup(html_file.read(), 'html.parser')

            # Basic info
            individual_officer_data['Basic Info'] = {
                'Name': soup.find(id='Label1').text,
                'Service': soup.find(id='Label2').text,
                'Cadre/Allotment Year': soup.find(id='Label3').text,
                'Date of Birth': soup.find(id='Label4').text,
                'Gender': soup.find(id='Label5').text,
                'Place of Domicile': soup.find(id='lblDomicile').text,
                'Date of Appoinment': soup.find(id='Label6').text,
                'Recruitment Source': soup.find(id='Label8').text,
                'IFS Cadre': soup.find(id='Label9').text, }

            # Educational Qualifications
            qualifications = soup.find(id='GridView1').find_all('td')
            individual_officer_data['Educational Qualifications'] = {
                'Qualification I': qualifications[0].text.replace(u'\xa0', u'none'),
                'Qualification II': qualifications[1].text.replace(u'\xa0', u'none'),
                'Qualification III': qualifications[2].text.replace(u'\xa0', u'none')}

            # Posting Details
            individual_officer_data['Posting Details'] = {}
            postings = soup.find(id='GridView2')
            if postings:  # check for Not Available
                postings = postings.find_all('tr')
                # first row is labels
                labels = [item.text for item in postings[0].find_all('th')]
                postings = postings[1:]
                for i, posting in enumerate(postings):
                    line_data = [item.text for item in posting.find_all('td')]
                    posting_data_dict = dict(zip(labels, line_data))
                    individual_officer_data['Posting Details'][i] = posting_data_dict

            # Training Details
            individual_officer_data['Training Details'] = {}
            trainings = soup.find(id='GridView3')
            if trainings:  # check for Not Available
                trainings = trainings.find_all('tr')
                # first row is labels
                labels = [item.text for item in trainings[0].find_all('th')]
                trainings = trainings[1:]
                for i, training in enumerate(trainings):
                    line_data = [item.text for item in training.find_all('td')]
                    training_data_dict = dict(zip(labels, line_data))
                    individual_officer_data['Training Details'][i] = training_data_dict
            # Specialization Details (Domestic)
            individual_officer_data['Specialization Details (Domestic)'] = {}
            specializations = soup.find(id='GridView4')
            if specializations:  # check for Not Available
                specializations = specializations.find_all('tr')
                # first row is labels
                labels = [
                    item.text for item in specializations[0].find_all('th')]
                specializations = specializations[1:]
                for i, specialization in enumerate(specializations):
                    line_data = [
                        item.text for item in specialization.find_all('td')]
                    specialization_data_dict = dict(zip(labels, line_data))
                    individual_officer_data['Specialization Details (Domestic)'][
                        i] = specialization_data_dict

        all_officer_data[html_filename.strip(
            '.html')] = individual_officer_data

    # Pretty print Python Dict to JSON file
    output_folder = os.path.join(data_folder_path, 'IFS-JSON')
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    output_file_absolute = os.path.join(output_folder, OUTPUT_FILE)
    with open(output_file_absolute, 'w') as file:
        file.write(json.dumps(all_officer_data, sort_keys=True, indent=4))

    print(
        f'Wrote {len(all_officer_data.keys())} keys to file {output_file_absolute}')


if __name__ == "__main__":
    main()
