# building_feature_extraction

## 1) Training Data Request Preparation

Scripts:
<ul>
<li>query.py: request OSM data</li>
<li>1_decompress.py: .pbf to .osm</li>
<li>Obtain boundary .kml file</li>
<li>3_subregion.py: keep only the OSM data located inside the boundary</li>
<li>4_filter_and_geotag.py: keep only OSM data with specific tags and geotag the data</li>
<li>sample_and_visualize.ipynb: obtain samples of each building type for training</li>
<li>infer_type.py: assign building type based on the number of connected buildings</li>
</ul>
