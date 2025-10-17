## 1.ADDRESS_DISTANCE_NEAR
from math import sin, asin, cos, radians, sqrt

class GeoDistanceCalculator:
    """
    地理距离计算器，用于计算两个地理坐标点之间的距离。
    """
    EARTH_RADIUS = 6372797.0  # 地球赤道半径，单位为米

    @staticmethod
    def calculate_distance(lat1, lon1, lat2, lon2):
        """
        计算两个地理坐标点之间的距离。

        参数:
        lat1, lon1 -- 第一个地点的纬度和经度
        lat2, lon2 -- 第二个地点的纬度和经度

        返回:
        两点之间的距离，单位为米。
        """
        # 将经纬度转换为弧度
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        # 计算纬度差和经度差
        dlat = abs(lat2 - lat1)
        dlng = abs(lon2 - lon1)
        # 根据半正矢公式计算两点间的距离
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlng/2)**2
        c = 2 * asin(sqrt(a))
        # 计算最终距离
        distance = GeoDistanceCalculator.EARTH_RADIUS * c
        return distance