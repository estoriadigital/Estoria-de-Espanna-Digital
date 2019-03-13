"""Bake pages."""

import webbrowser
import json
import os
import time

START = 800
STOP = 800
DELAY = 4
HOST = "http://estoria.example.com"
#HOST = "http://estoria.bham.ac.uk"


LIST_FILE = "collations.json"
PATH = "/edition/apparatus/chapter/?chapter=%s&bake=yes"
URL = HOST + PATH


class Baker(object):
    """Bake pages into HTML."""
    def __init__(self):
        with open(LIST_FILE) as list_fo:
            collations = json.load(list_fo)
        extras = []
        collation_list = []
        for item in collations.keys():
            try:
                collation_list.append(int(item))
            except ValueError:
                extras.append(item)
        collation_list.sort()
        collation_list.extend(extras)
        self.collations = collation_list


    def process(self):
        """Get all the pages."""
        for index, page_number in enumerate(self.collations[START:]):
            self.process_page(page_number)
            #if index > 0 and index % 20:
            #    os.system('killall x-www-browser')

    def process_page(self, page_number):
        """Process a single page."""
        url = URL % page_number
        webbrowser.open(url)
        time.sleep(DELAY)

if __name__ == '__main__':
    BAKER = Baker()
    BAKER.process()
