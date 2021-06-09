#!/usr/bin/env python
# coding: utf-8

# Infer a more specific building type than 'house' from the number
# of connected buildings obtained using Overpass API
# Inputs:
# - .csv of OSM data with way IDs
# Outputs:
# - .csv of the same OSM data with inferred building type

import csv
import json
import requests
import os
import time
import sys

# input/output filenames
input_filename = 'building_house_sample_2000_v2.csv'
output_filename = 'inferred_building_house_sample_2000_v2.csv'

overpass_url = "http://overpass-api.de/api/interpreter"


def infer_type(row):
    try:
        overpass_query = f'[out:json];(way({row["id"]});complete{{way(around:0)["building"];}};)->.r;.r out count;'
        r = requests.get(overpass_url, params={'data': overpass_query})
        r.raise_for_status()
        r_dict = r.json()
        num_connected_buildings = int(r_dict['elements'][0]['tags']['total'])
        if num_connected_buildings <= 1:
            row['osm_tag'] = 'detached'
        elif num_connected_buildings == 2:
            row['osm_tag'] = 'semi_detached_house'
        elif num_connected_buildings > 2:
            row['osm_tag'] = 'row_house'
        row['attached_buildings'] = num_connected_buildings
    except:
        pass


if os.path.isfile(output_filename):
    print('File with name output_filename already exists.')
else:
    with open(input_filename, newline='') as inputfile:
        reader = csv.DictReader(inputfile)
        with open(output_filename, 'w', newline='') as outputfile:
            fieldnames = reader.fieldnames
            fieldnames.append('attached_buildings')
            writer = csv.DictWriter(outputfile, fieldnames=fieldnames)
            writer.writeheader()
            for row_num, row in enumerate(reader):
                if 577 <= row_num < 1000:
                    infer_type(row)
                    writer.writerow(row)
                    time.sleep(1)
                    print(f'{row_num}/1000 completed.')
                elif row_num >= 1000:
                    break

print('Done.')
