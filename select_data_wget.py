# Command Line Implementation

import os
import gzip
import shutil


zip_out = "ottawa.osm.gz"
query = "ottawa.ql"

command = "wget -O {0} --header='Accept-Encoding: gzip, deflate' --post-file={1} 'https://overpass-api.de/api/interpreter'".format(
    zip_out, query
)
os.system(command)

with gzip.open(zip_out, "rb") as f_in:
    with open("ottawa.osm", "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)
