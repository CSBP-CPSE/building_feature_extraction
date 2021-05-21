import requests
import xml.etree.ElementTree as ET

boundary_rel_id = 4136816  # OSM Relation ID of boundary
output_boundary_file = f'2b-input-{boundary_rel_id}-boundary-nodes.osm'  # nodes only
overpass_url = "http://overpass-api.de/api/interpreter"
overpass_query = f'[out:xml];(rel(id:{boundary_rel_id})->.a;way(r.a)->.b;node(w.b)->.c;);.c out geom;'

if os.path.isfile(output_boundary_file):
    print('File with name output_boundary_file already exists.')
else:
    response = requests.get(overpass_url, params={'data': overpass_query})
    tree = ET.fromstring(response.content)
    with open(output_boundary_file, "wb") as f:
        f.write(ET.tostring(tree))
print('Done.')
