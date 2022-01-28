"""
This script is used to create the chapter index (indice in Spanish) that
appears on the right hand side of the edition home page.

The chapter index data is provided in a csv file (spreadsheet) at /srv/estoria/

* The first column of the ingest data is to be ignored. It refers to an old and
incorrect numbering system.
* The second column is the @n value of the div in the XML transcriptions.
* The third is the PCG chapter number (referring to a printed edition)
* The fourth is the title of the chapter.
* If the title reads Not to be included in the list of chapters' then that line
of data should be ignored.

We also need to know what page of each manuscript each chapter starts on so
that the correct page can be opened using the index.

This data is extracted from the paginated data that is used in the webpage to
display the transcriptions. If any of the pagination has changed in the
transcriptions it is essential that the paginated data is rebuilt before
running this script.

The list of manuscript sigla in the variable 'manuscripts' is used to ensure the
manuscripts appear in a fixed order in the dropdown menus in the index. It
should contain all manuscript in the order they need to appear.

Run in python3
No further arguments required

"""

import os
import json
from lxml import etree

xml_dir = '../../transcriptions/manuscripts'
index_file = '../../chapter_index.csv'
output_file = '../static/data/indice.json'
page_dir = '../transcription'

manuscripts = os.listdir('../transcription')

#This section makes the initial json of the index from the csv file with
#placeholders for manuscripts extant and pages
print('reading chapter index data')
lines = open(index_file, 'r', encoding='utf-8').readlines()
indice = {}
position = 1

for line in lines:

    tabs = line.split('\t')
    div = tabs[1].strip()
    PCG = tabs[2].strip()
    title = tabs[3].strip()
    if title != 'Not to be included in the list of chapters':

        indice[position] = {'title': title,
                            'div': div,
                            'PCG': PCG,
                            'manuscripts': [],
                            'pages': {}}
        position += 1

# read Ss and grab all VC_ chapters (add cxxxix (missing in Ss before cxl)
filename = os.path.join(xml_dir, 'Ss.xml')
parser = etree.XMLParser(resolve_entities=False, encoding='utf-8')
tree = etree.parse(filename, parser)

for chapter in tree.xpath('//div[@n]'):
    if chapter.get('n').find('VC_') == 0:
        n = chapter.get('n').replace('VC_', '')
        if n == 'cxl':
            indice[position] = {'title': '',
                                'div': 'cxxxix',
                                'PCG': 'cxxxix',
                                'manuscripts': [],
                                'pages': {}}
            position += 1

        indice[position] = {'title': '',
                            'div': n,
                            'PCG': n,
                            'manuscripts': [],
                            'pages': {}}
        position += 1


print('collecting manuscript page data')
#This section works out which divs start on which page of each manuscript
manuscript_pages = {}
for ms in manuscripts:
    print(ms)
    manuscript_pages[ms] = {}
    for pagefile in os.listdir(os.path.join(page_dir, ms)):
        if pagefile.endswith('.json'):
            with open(os.path.join(page_dir, ms, pagefile), encoding="utf-8") as file_p:
                page = json.load(file_p)
            try:
                root_element = etree.fromstring(page['text'])
            except etree.XMLSyntaxError:
                print("Not parsing xml of %s, %s" % (ms, pagefile))
            else:
                divs = root_element.findall('.//div[@n]')
                for div in divs:
                    if 'continued' not in div.attrib:
                        manuscript_pages[ms][div.attrib['n'].replace('VC_', '')] = pagefile.replace('.json', '')
# print(manuscript_pages)
#now we add manuscript page details to the index
for pos in indice:
    div_id = indice[pos]['div']
    for ms in manuscripts:
        if div_id in manuscript_pages[ms]:
            indice[pos]['manuscripts'].append(ms)
            indice[pos]['pages'][ms] = manuscript_pages[ms][div_id]

with open(output_file, 'w', encoding="utf-8") as output:
    output.write(json.dumps(indice))
