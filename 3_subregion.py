# This script takes as input a .osm file of all nodes, ways, and relations and a kml file that defines a boundary.
# The output is a .osm file of the nodes and ways from the input .osm that are inside the boundary.

from fastkml import kml
import os
import osmium as o
from pyproj import Proj, itransform
from shapely import wkt
from shapely.geometry import LineString, Polygon, Point
import matplotlib.pyplot as plt


# Input/Output Filenames & Projections
kml_input_filename = "3-input-ottawa-boundary.kml"  # boundary
input_osm_data = '3-input-ontario-nwr.osm'  # all osm data for a region
output_subregion_osm_data = '4-input-ottawa-nw.osm'
# Geocoordinates projection
p1 = Proj('+init=epsg:4326')
p2 = Proj('+proj=lcc +lon_0=-97.734375 +lat_1=47.6583799 +lat_2=76.5041114 +lat_0=62.0812457 +datum=WGS84 +units=m +no_defs')  # conformal projection


# Read kml file and project boundary coordinates.
with open(kml_input_filename, 'rb') as myfile:
    doc=myfile.read()
k = kml.KML()
k.from_string(doc)
kml_polygon = list(list(k.features())[0].features())[0].geometry.exterior.coords
boundary_lnglat = [(point[0], point[1]) for point in kml_polygon]  # list of (lon, lat)
boundary_xy = [node for node in itransform(p1, p2, boundary_lnglat, switch=True)]
# x = [p[0] for p in boundary_xy]
# y = [p[1] for p in boundary_xy]
# plt.plot(x,y)
# plt.show()
boundary_poly_xy = Polygon(boundary_xy)  # Polygon to used as boundary shape below

# write new .osm file.
class DataWriter(o.SimpleHandler):
    def __init__(self, writer):
        o.SimpleHandler.__init__(self)
        self.writer = writer

    def node(self, n):
        try:
            node_point_xy = Point(list(itransform(p1, p2, [(n.location.lon, n.location.lat)], switch=True)))
            if node_point_xy.within(boundary_poly_xy):
                self.writer.add_node(n)
        except:
            pass
        
    def way_centroid(self, w):
        nodes_lnglat = list(wkt.loads(wkt_factory.create_linestring(w.nodes)).coords)
        nodes_xy = list(itransform(p1, p2, nodes_lnglat, switch=True))
        centroid_xy = LineString(nodes_xy).centroid
        centroid_xy = Point(round(centroid_xy.x, 7), round(centroid_xy.y, 7))
        return centroid_xy

    def way(self, w):
        try:
            way_centroid_point_xy = self.way_centroid(w)
            if way_centroid_point_xy.within(boundary_poly_xy):
                self.writer.add_way(w)
        except:
            pass


if os.path.isfile(output_subregion_osm_data):
    print('File with name output_subregion_osm_data already exists.')
else:
    wkt_factory = o.geom.WKTFactory()
    writer = o.SimpleWriter(output_subregion_osm_data)
    h = DataWriter(writer)
    h.apply_file(input_osm_data, locations=True)
    writer.close()
print('Done.')
