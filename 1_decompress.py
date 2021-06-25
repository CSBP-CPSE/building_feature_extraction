#!/usr/bin/env python
# coding: utf-8

# .pbf to .osm
# Inputs:
# - .pbf of OSM data
# Outputs:
# - .osm of the same OSM data

import osmium as o

input_file = 'ontario-latest.osm.pbf'
output_file = '3-input-ontario-nwr.osm'


class Convert(o.SimpleHandler):

    def __init__(self, writer):
        super(Convert, self).__init__()
        self.writer = writer

    def node(self, n):
        self.writer.add_node(n)

    def way(self, w):
        self.writer.add_way(w)

    def relation(self, r):
        self.writer.add_relation(r)

if os.path.isfile(output_file):
    print('File with name output_file already exists.')
else:
    writer = o.SimpleWriter(output_file)
    handler = Convert(writer)
    handler.apply_file(input_file)
    writer.close()
print('Done.')
