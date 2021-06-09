#!/usr/bin/env python
# coding: utf-8

# Use Overpass API to get OSM data
# Can be used to obtain all data in a boundary
# Inputs:
# - overpass_query -> Overpass API query
# Outputs:
# - .osm of the query results

import requests
import json
import os.path
from xml.etree import ElementTree

output_filename = 'output-query-data.osm'
overpass_url = "http://overpass-api.de/api/interpreter"
overpass_query = """

"""

if os.path.isfile(output_filename):
    print('File with name output_filename already exists.')
else:
    with requests.get(overpass_url, params={'data': overpass_query}, headers={'Accept-Encoding': 'gzip, deflate'}, stream=True) as r:
        r.raise_for_status()
        with open(output_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                f.write(chunk)
print('Done.')
