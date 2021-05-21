# Requests Module Implementation

import requests
import json
from xml.etree import ElementTree

output_filename = "overpass_output.xml"

overpass_url = "http://overpass-api.de/api/interpreter"

overpass_query = """
[out:xml];
area[name="Ottawa"];
(
  nwr(area);
  node(w);
);
out geom;
"""

headers = {
    "accept-encoding": "gzip, deflate",
}

with requests.get(
    overpass_url, params={"data": overpass_query}, headers=headers, stream=True
) as r:
    r.raise_for_status()
    with open(output_filename, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
