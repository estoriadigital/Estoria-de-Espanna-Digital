"""
This script makes two files. The have the same data a slightly different structure.
The data is the collation editor output stored in /srv/estoria/edition/apparatus/collation

One is a json object used by make_apparatus_index_page.py to generate the main 
apparatus index. 
This file is saved to /srv/estoria/edition/apparatus/collations.json

The other is a javascript file containing a variable called COLLATION_LIST
which contains the same json object as the file above. This is used to generate 
the chapter views of the critical text.
This file is saved to /srv/estoria/edition/static/data/collations.js

"""

import os
import json

def main():
    blobs = [filename.strip('.json') for filename in os.listdir('../apparatus/collation')]
    blobs.sort()
    data = {}

    for blob in blobs:
        if blob == 'DS_Store':
            continue
        if 'S' in blob:
            something = blob.split('S')

            verse = something[1]
            chapter = something[0].upper().lstrip('D')
            if verse == "400>":
                print(something)
                verse = 400.1
            elif verse == "659.1":
                print(something)
                verse = 659.1

            try:
                chapter = int(chapter)
            except ValueError:
                print("Choked on", chapter)
                pass
            if not chapter in data:
                data[chapter] = []
            try:
                verse = int(verse)
            except ValueError:
                pass

            if verse == 'RUBRIC':
                verse = 'Rubric'
            if verse == 'rubric':
                verse = 'Rubric'

            if verse == 'Rubric':
                data[chapter].insert(0, verse)
            else:
                data[chapter].append(verse)
                rubric = False
                if 'Rubric' in data[chapter]:
                    data[chapter].remove('Rubric')
                    rubric = True

                try:
                    data[chapter].sort()
                except TypeError:
                    print(chapter, verse, data[chapter])

                if rubric:
                    data[chapter].insert(0, 'Rubric')

        else:
            continue

    with open('../apparatus/collations.json', 'w') as fp:
        json.dump(data, fp, indent=4)
    with open('../static/data/collations.js', 'w') as js_file:
        js_file.write('COLLATION_LIST = ')
        json.dump(data, js_file, indent=4)

if __name__ == '__main__':
    main()
