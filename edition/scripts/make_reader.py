"""
This script makes the readers edition which is stored as html files by chapter
in the /srv/estoria/edition/reader directory. Resulting file names are
[chapter_number].html

The reader.xml file should be put in /srv/estoria/transcirptions/readerXML

At the same time this file creates the index data used for the VPL dropdown
which is saved at /srv/estoria/edition/static/data/reader_pages.js

"""
import os
import shutil
import json
from lxml import etree


DIR = '../../transcriptions/readerXML'
RUBRIC_TEMPLATE = '<span class="rubric">%s</span><br />\n'

class Reader(object):
    """Make Reader edition pages."""
    def __init__(self):
        self.tree = etree.fromstring(open(os.path.join(DIR, 'reader.xml'), 'r', encoding="utf-8").read())
        self.page_list = []

    def process(self):
        """Process all the pages."""
        print('creating new reader pages')
        for div in self.tree.xpath('//tei:div[@type="book"]/tei:div',
                                   namespaces={'tei': 'http://www.tei-c.org/ns/1.0'}):
            self.process_page(div)
            #sys.exit()
        with open(os.path.join('../static/data', 'reader_pages.js'), 'w', encoding="utf-8") as list_fo:
            list_fo.write('READER_PAGES = ')
            json.dump(self.page_list, list_fo, indent=4)

    def get_text(self, block):
        """ """
        hitags = block.findall("hi")
        spaces = block.findall("space")
        if not hitags and not spaces:
            return block.text
        text = ""
        for element in block.iter():
            if element.tag == 'ab':
                if element.text:
                    text += element.text
            if element.tag == 'hi':
                if element.text:
                    if element.get('rend'):
                        rend = element.get('rend')
                    else:
                        rend = ""
                    text += ' <span class="hi %s">%s</span>' % (rend, element.text)
                if element.tail:
                    text += element.tail
            if element.tag == 'space':
                text += '<span class="space" />'
                if element.tail:
                    text += element.tail
        return text

    def process_page(self, div):
        """Process a single page."""
        has_opening_rubric = False
        has_closing_rubric = False

        first_rubric = div.getchildren()[0]
        last_rubric = div.getchildren()[-1]
        has_opening_rubric = first_rubric.attrib['n'].lower() == "rubric"
        if last_rubric.attrib['n'].lower() == "rubric":
            if first_rubric != last_rubric:
                has_closing_rubric = True

        name = div.get('n')
        output = '<span class="chapter">%s</span>\n' % name

        if has_opening_rubric:
            output += RUBRIC_TEMPLATE % first_rubric.text
            if has_closing_rubric:
                blocks = div.getchildren()[1:-1]
            else:
                blocks = div.getchildren()[1:]
        else:
            blocks = div.getchildren()

        for block in blocks:
            block_n = block.get('n')
            #text = block.text
            text = self.get_text(block)
            output += '<span id="%s"><sub>%s</sub>%s</span>\n' % (block_n,
                                                                  block_n,
                                                                  text)

        if has_closing_rubric:
            output += '<br />'
            output += RUBRIC_TEMPLATE % last_rubric.text


        self.page_list.append(name)
        with open('../reader/%s.html' % name, 'w', encoding="utf-8") as output_fo:
            output_fo.write(output)

    def clear_reader_directory(self):
        try:
            shutil.rmtree('../reader')
        except:
            pass
        try:
            os.mkdir('../reader')
        except FileExistsError:
            pass
        print('old reader pages deleted')

if __name__ == "__main__":
    READER = Reader()
    READER.clear_reader_directory()
    READER.process()
