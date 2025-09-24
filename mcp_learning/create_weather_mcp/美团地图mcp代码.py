import os
import os
from typing import List, Union

import httpx
from mcp.server.fastmcp import FastMCP, Context

# 创建MCP服务器实例
mcp = FastMCP("meituan-map")

# 设置API密钥，从美团地图开放平台获取
api_key = os.getenv('MEITUAN_MAPS_API_KEY')
api_url = "https://lbsapi.meituan.com"


@mcp.tool()
async def geocoding_v1(
        address: str,
        city: str = None,
        scenario: str = "GENERAL"
) -> dict:
    """
    Name:
        地理编码服务

    Description:
        将结构化地址转换为经纬度坐标。地址结构越完整，解析精度越高。

    Args:
        key: 请求服务权限标识，用户申请的Web服务API Key
        address: 结构化地址信息，省+市+区+街道+门牌号，其中省+市+区县必填
        city: 查询所在的城市，支持city汉字的形式
        scenario: 应用场景(GENERAL/POICHECK/COMPATIBILITY/POIMINING)，默认GENERAL
    """
    try:
        # 获取API密钥
        if not api_key:
            raise Exception("API key is not set")
        # 调用美团API
        url = f"{api_url}/v1/location/geo"
        params = {
            "key": api_key,
            "address": address,
            "from": "py_mcp"
        }

        # 添加可选参数
        if city:
            params["city"] = city
        if scenario:
            params["scenario"] = scenario

        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            result = response.json()

        if result.get("status") != 200:
            error_msg = result.get("msg", "unknown error")
            raise Exception(f"API response error: {error_msg}")

        # 只保留location和level字段
        filtered_result = {
            "status": result.get("status"),
            "msg": result.get("msg"),
            "count": result.get("count", 0),
            "geocodes": [],
            "source": result.get("source")
        }

        for geocode in result.get("geocodes", []):
            filtered_geocode = {
                "location": geocode.get("location"),
                "level": geocode.get("level")
            }
            filtered_result["geocodes"].append(filtered_geocode)

        return filtered_result

    except httpx.HTTPError as e:
        raise Exception(f"HTTP request failed: {str(e)}") from e
    except KeyError as e:
        raise Exception(f"Failed to parse response: {str(e)}") from e


@mcp.tool()
async def regeo_v1(
        location: str,
        radius: int = 50,
        scenario: str = "GENERAL",
        limit: int = 10,
) -> dict:
    """
    Name:
        位置描述（逆地理编码）服务

    Description:
        将经纬度坐标转换为结构化地址。

    Args:
        location: 经纬度坐标，格式为 "lng,lat"，如 "116.397537,39.906834"
        radius: 搜索半径，默认为200,最大只为 200,单位：米
        scenario: 应用场景，默认为 GENERAL
        limit: 返回条数控制，默认为 10，最大值为 20
    """
    try:
        if not api_key:
            raise Exception("API key is not set")

        url = f"{api_url}/v1/location/regeo"
        params = {
            "key": api_key,
            "location": location,
            "radius": radius,
            "scenario": scenario,
            "limit": limit,
            "show_fields": "base|admin|poi",
            "from": "py_mcp"
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            result = response.json()

        if result.get("status") != 200:
            error_msg = result.get("msg", "unknown error")
            raise Exception(f"API response error: {error_msg}")

        # 去掉POI信息中的mtid和dpid字段
        for regeocode in result.get("regeocode", []):
            for poi in regeocode.get("pois", []):
                if "mtid" in poi:
                    del poi["mtid"]
                if "dpid" in poi:
                    del poi["dpid"]
                if "type" in poi:
                    del poi["type"]
        return result

    except httpx.HTTPError as e:
        raise Exception(f"HTTP request failed: {str(e)}") from e
    except KeyError as e:
        raise Exception(f"Failed to parse response: {str(e)}") from e


@mcp.tool()
async def driving_route_v1(
        origin: str,
        destination: str,
        waypoints: str = None,
        strategy: str = "RECOMMEND",
        multipath: int = 1,
) -> dict:
    """
    驾车路线规划服务

    Args:
        origin: 起点经纬度坐标，格式为 "lng,lat"
        destination: 终点经纬度坐标，格式为 "lng,lat"
        waypoints: 途经点列表，格式为 "lng1,lat1;lng2,lat2"
        strategy: 路线策略，默认为 RECOMMEND
        multipath: 返回路径数量，默认为 1
    """
    return await route_planning("driving", origin, destination, waypoints, strategy, multipath, "distance|duration")


@mcp.tool()
async def riding_route_v1(
        origin: str,
        destination: str,
        waypoints: str = None,
        strategy: str = "S",
        multipath: int = 1,
) -> dict:
    """
    骑行路线规划服务

    Args:
        origin: 起点经纬度坐标，格式为 "lng,lat"
        destination: 终点经纬度坐标，格式为 "lng,lat"
        waypoints: 途经点列表，格式为 "lng1,lat1;lng2,lat2"
        strategy: 路线策略，默认为 S(完全合规)
        multipath: 返回路径数量，默认为 1
    """
    return await route_planning("riding", origin, destination, way
