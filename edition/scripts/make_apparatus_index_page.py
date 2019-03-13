"""
This script generates the apparatu index found at /edition/apparatus/list 
(/srv/estoria/edition/apparatus/list/index.html)

The data for chapter and verse is pulled from the collations.json file in the 
apparatus directory.

"""

import os
import json
import collections

HEADER = """
<!DOCTYPE html>
<html lang="en"> <!-- Set this to the main language of your site -->
<head>
    <meta charset="utf-8">
    <title>Estoria Apparatus Demo</title>
    <link rel="stylesheet" href="../estoria.css" type="text/css">

  </head>
  <body>

    <h1>Estoria Apparatus Demo</h1>
    <p>Very simple view. Just to check we are getting the right text.</p>
    <p>Note, words are in the German numbering (words are even, spaces are odd).</p>
"""

FOOTER = """
  </body>
</html>"""


#CODE_LINE = """    <p>%s (%s) (<a href="/edition/apparatus/chapter/?chapter=%s&display=%s">whole chapter</a>)  (<a href="/edition/apparatus/chapter/?chapter=%s&display=%s&bake=yes">bake</a>)</p>"""

CODE_LINE = """    <p>%s (<a href="/edition/apparatus/chapter/?chapter=%s">whole chapter</a>)  (<a href="/edition/apparatus/chapter/?chapter=%s&bake=yes">bake</a>)</p>"""

def main():
    
    with open('../apparatus/collations.json') as fp:
        data = json.load(fp, object_pairs_hook=collections.OrderedDict)
        
    with open('../apparatus/list/index.html', 'w') as index_file:
        index_file.write(HEADER)
        
        for chapter in data:
            index_file.write(CODE_LINE % (chapter, chapter, chapter))
            index_file.write("    <ul>")
            
            for verse in data[chapter]:
                context = "D%sS%s" % (chapter, verse)
                index_file.write("""      <li>%s | <a href="/edition/apparatus/?context=%s">Critical Edition</a> </li>""" % (verse, context))
            index_file.write("    </ul>")
    
        index_file.write(FOOTER)


def old_main():
    with open('/srv/estoria/edition/apparatus/collations.json') as fp:
        data = json.load(fp, object_pairs_hook=collections.OrderedDict)
        
    with open('../apparatus/list/index.html', 'w') as index_file:
        index_file.write(HEADER)
    
        for index, chapter in enumerate(data):
            index_file.write(CODE_LINE % (index+1,
                               chapter,
                               chapter,
                               index+1,
                               chapter,
                               index+1))
            index_file.write("    <ul>")
            for verse in data[chapter]:
                context = "D%sS%s" % (chapter, verse)
                index_file.write("""      <li>%s | <a href="/edition/apparatus/?context=%s">Critical Edition</a> | <a href="/edition/apparatus/editor/?context=%s">Reader Edition</a> </li>""" % (verse,context,context))
            index_file.write("    </ul>")
    
        index_file.write(FOOTER)

if __name__ == '__main__':
    main()
    
