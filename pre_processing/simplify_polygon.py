import fiona
from shapely.geometry import shape, mapping
from fiona.crs import from_epsg

# 路径设置
input_file = "../data/LGA_POLYGON.shp"
output_file = "../data/0.99_LGA_POLYGON.shp"

tolerance = 0.99

with fiona.open(input_file, 'r') as input:
    schema = input.schema.copy()
    crs = input.crs

    with fiona.open(output_file, 'w', 'ESRI Shapefile', schema=schema, crs=crs) as output:
        for elem in input:
            geom = shape(elem['geometry'])

            simplified_geom = geom.simplify(tolerance, preserve_topology=True)

            output.write({
                'properties': elem['properties'],
                'geometry': mapping(simplified_geom)
            })

print("Polygon simplification is complete. Output saved to", output_file)
