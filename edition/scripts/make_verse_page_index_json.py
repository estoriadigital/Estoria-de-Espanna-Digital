#!/usr/bin/python3

"""



"""
import os
import json
from lxml import etree

PAGE_LOCATION = "../transcription"
index = {}

def get_verses(xml, ms, page_num):
    tree = etree.fromstring(xml)
    for chapter in tree.findall('.//div'):
        chapter_num = chapter.get('n')
        for verse in chapter.findall('.//ab'):
            if verse.get('continued'):
                pass
            else:
                verse_num = verse.get('n')
                index[ms]['D%sS%s' % (chapter_num, verse_num)] = page_num
        

def main():
    for ms in os.listdir(PAGE_LOCATION):
        dir_path = os.path.join(PAGE_LOCATION, ms)
        print(ms)
        index[ms] = {}
        for page in os.listdir(dir_path):
            if page.endswith('.json'):
                filename = os.path.join(PAGE_LOCATION, ms, page)
                with open(filename) as file_p:
                    data = json.load(file_p)
                    get_verses(data['text'], ms, page.replace('.json', ''))
    #write out the results
    with open('../apparatus/chapter/page_chapter_index.js', 'w') as output:
        output.write('PAGE_CHAPTER_INDEX = ')
        json.dump(index, output, indent=4)
    
if __name__ == '__main__':
    main()