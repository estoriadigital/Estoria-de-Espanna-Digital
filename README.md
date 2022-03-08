Introduction
----
This repository contains the scripts and data (excluding transcription data and
images) which was used to create the Estoria de Espanna digital edition. The XML
transcription data is available in the Transcription repository which is
included as a submodule. The copyright of the images prevents them from being
shared openly.

It is not intended that this repository can be used to recreate Estoria Digital.
Rather it is made available here to illustrate how the edition was put together
and so that components that are useful to others can be reused.

Requirements (css and js)
----
* jQuery
* jQuery-ui
* Bootstrap
* MetisMenu
* Tooltipster
* Gridstack
* font-awesome



Structure of the repository
----

All of the files that make up the edition itself are in the `edition` directory.

Files at the same level as this directory are the raw data files.

To copy the structure used for the Estoria Digital the manuscript transcriptions
should be added in a directory named `XML` and the `reader.xml` file should be
added in a directory named `readerXML`. Both of these directories should be at
the same level as the `edition` directory. Sym links should also be created as
follows: * `edition/transcription` -> `edition/static/data/transcription` *
`edition/reader` -> `edition/static/data/reader` * `edition/critical` ->
`edition/static/data/critical`

The `edition` directory contains the processed transcription and collation data
and the static files necessary for the edition. The `scripts` directory provides
all of the scripts that turn the raw data into the data used in the edition. The
'baking' process referred to in the documentation of the scripts below is now
done by the code available in the estoria-admin repository.

Files in the `edition/apparatus` directory are no longer used as these functions
have been replaced by the functions in the estoria-admin repository. The files
are included here to document how the original Estoria digital edition was made.


Building the edition
----

All scripts must be run with Python3. Further documentation can be found at the
top of each script.


### How to upload transcriptions


* Name each file with the witness sigla followed by '.xml'
* Put the XML files in the `transcriptions/manuscripts` directory (`transcriptions` is a git submodule)
* Navigate to the `edition/scripts` directory
* Make the pages by doing the following:
  * Run `make_paginated_json.py`
  * Run `add_html_to_paginated_json.py`
* Make the chapter index by running `make_chapter_index_json.py`



### How to upload the reader text


* Name the XML file 'reader.xml'
* Put the XML file in the `transcriptions/readerXML` directory (`transcriptions` is a git submodule)
* Navigate to the `edition/scripts` directory
* Run make_reader.py


### The data for the dropdown menus for MS/VPL/VPE


The MS menu dropdown data all lives in the file `edition/static/data/menu_data.js`
This file is created as part of running the `edition/scripts/make_paginated_json.py`

The VPL menu dropdown data lives in the file `edition/static/data/reader_pages.js`
It is created as part of running the file `edition/scripts/make_reader.py` used to upload the reader text

The VPE menu dropdown data lives in the file `edition/static/data/critical_pages.js`
There is no script to make this but it is just a list of numbers so is not difficult to make.

Deprecated Processes
----

The processes documented here are no longer needed as this original process has
been replaced by the functions provided in the estoria-admin repository. It
remains here to explain how the original edition was made.

### The critical edition

The folder containing the approved collations needs to be sym linked to
`edition/apparatus/collation`

It is essential that all of the data in this folder is named correctly with
regards to D and S values and that the 'context' value in the json within these
files is also correct. The script `make_context_match_filename.py` was written
to fix problems caused by renumbering at various stages of the project. The
entire critical edition build relies on this being correct. It should be correct
now so this script should not be needed.

To check the critical apparatus and 'bake' the results into the VPE pages go to
estoria.bham.ac.uk/edition/apparatus/list

The page shown at that location can be found at `edition/apparatus/list/index.html`

This page allows you to select a chapter to see how it will appear in the final
edition. This is generated 'on the fly' using the index.html file in
`edition/apparatus/chapter` and the associated javascript and css files called
into this html file.

You can also look at a more detail version of each sentence. This is again
generated 'on the fly' using the index.html file in `edition/apparatus` and
associated javascript files at the same location including handlebars and
loadjson.js

The critical edition files are served as html files from` edition/static/data/critical/` this folder is
sym link to `edition/critical/` where the files really live.

These files are generated by the 'baking' process. Once each chapter has been
checked it can be baked using the second link in the edition index page. The
baking process does not currently run on the server. To run it locally you must
first start the server.py script at `edition/apparatus/baking/server.py`. This
will continue to run in the terminal window and allow the files to be baked
using `edition/apparatus/baker.py` (The host is hard coded in this file and will
need to be changed for this to run on the server).

### To generate the files required for the critical edition


There are lots of files needed to make the critical edition work. They sometimes
rely on each other so order is important.

To reproduce the entire critical edition do the following (each script is
documented at the top and that information is not repeated here):

* run `make_critical_chapter_verse_json.py` to make required js and json data files
* make a new index file for `edition/apparatus/list/index.html` by running `make_apparatus_index_page.py`
* bake any chapters that have changed (can only be done locally currently)
* Make the indice json by running `make_chapter_index_json.py`

Referencing
----
To cite the Estoria de Espanna code please use the DOI:
[![DOI](https://zenodo.org/badge/174379996.svg)](https://zenodo.org/badge/latestdoi/174379996)

Installation of new version
---
Needs nodejs installed

Clone the repository.
Navigate to the edition directory.
Install the node modules.
```bash
npm install
```

build the webpack package

```bash
npm run build
```

This builds all of the dependencies but not the data. The data now needs to be built.
