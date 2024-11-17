import pandas as pd

# Geo data provided
# geo_items = {
#     'Latitude': [22.894559689319834, 22.886376973309183],
#     'Longitude': [113.47484770222422, 113.4830306533438],
#     'X': [-1.4901161193847656e-7, 1142.998168796301],
#     'Y': [0, 1244.0001220703125]
# }
geo_items = {
    'Latitude': [22.890855656179056, 22.891966148227198],
    'Longitude': [113.47675370391693, 113.47839591270292],
    'X': [-148, 0],
    'Y': [-104, 0]
}


def get_lat_lon(x_coords, y_coords):
    """
    将X,Y坐标转换为经纬度坐标
    参数:
        x_coords: X坐标列表
        y_coords: Y坐标列表
    返回:
        经纬度坐标列表 [[longitude, latitude], ...]
    """
    geo_df = pd.DataFrame(geo_items)
    
    # 计算缩放因子
    delta_lat = geo_df['Latitude'][1] - geo_df['Latitude'][0]
    delta_lon = geo_df['Longitude'][1] - geo_df['Longitude'][0]
    delta_x = geo_df['X'][1] - geo_df['X'][0]
    delta_y = geo_df['Y'][1] - geo_df['Y'][0]

    scale_x = delta_x / delta_lon
    scale_y = delta_y / delta_lat

    # 计算偏移量
    offset_x = geo_df['X'][0] - geo_df['Longitude'][0] * scale_x
    offset_y = geo_df['Y'][0] - geo_df['Latitude'][0] * scale_y

    # 反向转换
    longitudes = [(x - offset_x) / scale_x for x in x_coords]
    latitudes = [(y - offset_y) / scale_y for y in y_coords]

    return [[lon, lat] for lon, lat in zip(longitudes, latitudes)]

if __name__ == "__main__":
    # 测试用例
    test_x = [3.40846, 5.86284, 8.61242, 10.8591, 12.8949, 14.5128, 14.608, 14.4159, 14.2624, 14.1309, 
            13.8495, 13.5317, 13.1734, 12.3821, 11.8829, 10.7689, 9.14096, 7.46202, 5.17498, 3.5499, 
            2.12156, -0.751957, -4.72415, -9.48917, -13.88, -16.9663, -18.5213, -17.9297, -15.5015, 
            -14.1887, -12.8965, -10.28, -10.075]
    test_y = [0.310959, 0.520711, 1.02445, 1.46648, 2.7159, 3.76708, 6.12391, 9.83308, 13.1887, 17.3503, 
            21.7159, 26.5505, 31.3486, 37.7716, 43.3149, 49.2677, 56.1847, 61.3525, 67.4001, 72.2888, 
            75.0279, 75.4357, 74.3781, 73.6926, 73.374, 73.5119, 75.3012, 78.363, 77.7082, 75.4853, 
            74.7625, 74.7467, 74.7468]
        
    result = get_lat_lon(test_x, test_y)
    print("转换结果 (经度,纬度):", result) 