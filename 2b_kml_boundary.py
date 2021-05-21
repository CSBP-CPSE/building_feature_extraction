#!/usr/bin/env python
# coding: utf-8

# TODO: complete conversion to .kml
import csv
import requests
import os
import osmium as o
import xml.etree.ElementTree as ET
import xmltodict

initial_boundary_file = f'2b-input-{boundary_rel_id}-boundary-nodes.osm'  # nodes only
boundary_nodes_lat_lon = f'{boundary_rel_id}_boundary_nodes.csv'

tree = ET.parse(initial_boundary_file)
xml_data = tree.getroot()
xmlstr = ET.tostring(xml_data, encoding='utf8', method='xml')
data_dict = dict(xmltodict.parse(xmlstr))['osm']['node']
list_data_dict = [{'lat':float(r['@lat']), 'lon':float(r['@lon'])} for r in data_dict]
keys = list_data_dict[0].keys()
with open(boundary_nodes_lat_lon, 'w', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, keys, extrasaction='ignore')
    dict_writer.writeheader()
    dict_writer.writerows(list_data_dict)
