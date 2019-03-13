import os
import json

def main():
    blobs = [filename.strip('.json') for filename in os.listdir('./collation')]
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

    with open('collations.json', 'w') as fp:
        json.dump(data, fp, indent=4)

if __name__ == '__main__':
    main()
