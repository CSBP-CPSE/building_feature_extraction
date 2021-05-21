import fiona
import alphashape
import csv
from shapely import geometry

points = []
with open("input_nodes.csv", "r") as input_file:
    reader = csv.reader(input_file)
    next(reader)
    for idx, row in enumerate(reader):
        points.append([float(row[1]), float(row[0])])


alpha = 0.95 * alphashape.optimizealpha(points)  # 0.182
hull = alphashape.alphashape(points, alpha)

schema = {
    "geometry": "Polygon",
    "properties": {"id": "int"},
}

# Write a new Shapefile
with fiona.open("final.shp", "w", "ESRI Shapefile", schema) as c:
    c.write(
        {
            "geometry": geometry.mapping(hull),
            "properties": {"id": 123},
        }
    )
