# Digital Land datasets

[![License](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/psd/openregister/blob/master/LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://black.readthedocs.io/en/stable/)

We recommend working in [virtual environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/) before installing the python dependencies:

    $ make init

The datasets are collected into the [collection](collection) directories:

    $ make

# Data

* [digital-land/dataset-collection/dataset/dataset.csv](https://github.com/digital-land/dataset-collection/blob/master/dataset/dataset.csv)

Information about organisations is taken from:

* [digital-land/organisation-collection/collection/organisation.csv](https://github.com/digital-land/organisation-collection/blob/master/collection/organisation.csv)
* [digital-land/organisation-collection/collection/tag.csv](https://github.com/digital-land/organisation-collection/blob/master/data/tag.csv)

You can change the URL for an individual file using an environment variable, for example:

    export brownfield_land_index=http://localhost:8000/brownfield-land-collection/collection/index.json

# Licence

The software in this project is open source and covered by LICENSE file.

Individual datasets copied into this repository may have specific copyright and licensing, otherwise all content and data in this repository is
[© Crown copyright](http://www.nationalarchives.gov.uk/information-management/re-using-public-sector-information/copyright-and-re-use/crown-copyright/)
and available under the terms of the [Open Government 3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/) licence.
