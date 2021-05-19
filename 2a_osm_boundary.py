import requests
import xml.etree.ElementTree as ET

boundary_rel_id = 4136816  # OSM Relation ID of boundary
initial_boundary_file = f'2b-input-{boundary_rel_id}-boundary-nodes.osm'  # nodes only
overpass_url = "http://overpass-api.de/api/interpreter"
overpass_query = f'[out:xml];(rel(id:{boundary_rel_id})->.a;way(r.a)->.b;node(w.b)->.c;);.c out geom;'

response = requests.get(overpass_url, params={'data': overpass_query})
tree = ET.fromstring(response.content)
with open(initial_boundary_file, "wb") as f:
    f.write(ET.tostring(tree))
