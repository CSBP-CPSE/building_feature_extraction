#!/usr/bin/env python
# coding: utf-8

import csv
import osmium as o
from pyproj import Proj, itransform
from shapely import wkt
from shapely.geometry import LineString
import sys


input_osm_data = '4-input-ottawa-nw.osm'
output_addresses = '5-input-filtered-geotagged.csv'
keep_tags = ['addr:housenumber', 'addr:street', 'building']

# Geocoordinates projection
p1 = Proj('+init=epsg:4326')
p2 = Proj('+proj=lcc +lon_0=-456.6796875 +lat_1=48.4823944 +lat_2=81.6964789 +lat_0=65.0894367 +datum=WGS84 +units=m +no_defs')  # conformal projection
# transformer = Transformer.from_crs(CRS('WGS84'), CRS(out_projection))


class LocationHandler(o.SimpleHandler):
    def __init__(self, writer):
        super(LocationHandler, self).__init__()
        self.writer = writer
    
    def node(self, n):
        try:
            node_tags = n.tags
            if all (k in node_tags for k in keep_tags):
                location_dict = {tag.k:tag.v for tag in node_tags}
                location_dict['latitude'] = round(n.location.lat, 7)
                location_dict['longitude'] = round(n.location.lon, 7)
                location_dict['osm_obj_type'] = 'node'
                writer.writerow(location_dict)
        except:
            pass
        
    def way_centroid(self, w):
        nodes_lnglat = list(wkt.loads(wkt_factory.create_linestring(w.nodes)).coords)
        nodes_xy = [node for node in itransform(p1, p2, nodes_lnglat, switch=True)]
        centroid_xy = LineString(nodes_xy).centroid
        centroid_xy = (round(centroid_xy.x, 7), round(centroid_xy.y, 7))
        centroid_latlng = p2(centroid_xy[1], centroid_xy[0], inverse=True)
        return centroid_latlng

    def way(self, w):
        try:
            way_tags = w.tags
            if all (k in way_tags for k in keep_tags):
                location_dict = {tag.k:tag.v for tag in way_tags}
                way_centroid = self.way_centroid(w)
                location_dict['latitude'] = round(way_centroid[0], 7)
                location_dict['longitude'] = round(way_centroid[1], 7)
                location_dict['osm_obj_type'] = 'way'
                writer.writerow(location_dict)
        except:
            pass

if os.path.isfile(output_addresses):
    print('File with name output_addresses already exists.')
else:
    with open(output_addresses, 'w', newline='', encoding='utf-8') as csvfile:
        wkt_factory = o.geom.WKTFactory()
        fieldnames = ['osm_obj_type', 'latitude', 'longitude', 'addr:unit']
        fieldnames.extend(keep_tags)
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        l = LocationHandler(writer)
        l.apply_file(input_osm_data, locations=True)
print('Done.')
