# building_feature_extraction

## 1) Training Data Request Preparation

Scripts:
<ul>
<li>1_decompress.py: .osm.pbf (all nodes, ways, relations) to .osm</li>
<li>2a_osm_boundary.py: get boundary nodes in a .osm given a relation id</li>
<li>2b_kml_boundary.py: (TODO) get boundary as .kml given .osm of boundary nodes</li>
<li>3_subregion.py: get .osm with nodes and ways from an input .osm that are inside a given .kml boundary</li>
<li>4_filter_and_geotag.py: get .csv with geotagged nodes and ways from input .osm that have specific tags</li>
<li>5_format.py: separate results into individual .csv for each value of a specific tag (e.g. one .csv for each value observed for the 'building' tag)</li>
</ul>
