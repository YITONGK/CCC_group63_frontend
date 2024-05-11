import fiona
from shapely.geometry import shape, mapping
from fiona.crs import from_epsg

# 路径设置
input_file = "../data/LGA_POLYGON.shp"
output_file = "../data/0.999_LGA_POLYGON.shp"

# 简化的容差设置
tolerance = 0.999

# 读取原始 Shapefile
with fiona.open(input_file, 'r') as input:
    # 创建一个新的 Shapefile 写入简化的几何数据
    schema = input.schema.copy()  # 复制原有 schema
    crs = input.crs  # 获取坐标参考系统

    with fiona.open(output_file, 'w', 'ESRI Shapefile', schema=schema, crs=crs) as output:
        for elem in input:
            # 转换为 Shapely 几何对象
            geom = shape(elem['geometry'])

            # 使用 Shapely 的简化方法
            simplified_geom = geom.simplify(tolerance, preserve_topology=True)

            # 将简化后的几何对象写入新文件
            output.write({
                'properties': elem['properties'],  # 保持属性不变
                'geometry': mapping(simplified_geom)
            })

print("Polygon simplification is complete. Output saved to", output_file)
