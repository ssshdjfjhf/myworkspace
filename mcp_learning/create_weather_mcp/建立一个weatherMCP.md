https://modelcontextprotocol.io/quickstart/server#set-up-your-environment

# 设置您的环境
首先，让我们安装uv并设置我们的 Python 项目和环境：

curl -LsSf https://astral.sh/uv/install.sh | sh

之后请确保重新启动终端以确保uv命令被接收。

现在，让我们创建并设置我们的项目：

# Create a new directory for our project
uv init weather
cd weather

# Create virtual environment and activate it
uv venv
source .venv/bin/activate

# Install dependencies
uv add "mcp[cli]" httpx

# Create our server file
touch weather.py

# 构建服务器
​
## 导入包并设置实例
将这些添加到您的顶部weather.py：
``
from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("weather")

# Constants
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"
``

FastMCP 类使用 Python 类型提示和文档字符串自动生成工具定义，从而轻松创建和维护 MCP 工具。

## 辅助函数
接下来，让我们添加辅助函数来查询和格式化来自国家气象局 API 的数据：
``
async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

def format_alert(feature: dict) -> str:
    """Format an alert feature into a readable string."""
    props = feature["properties"]
    return f"""
Event: {props.get('event', 'Unknown')}
Area: {props.get('areaDesc', 'Unknown')}
Severity: {props.get('severity', 'Unknown')}
Description: {props.get('description', 'No description available')}
Instructions: {props.get('instruction', 'No specific instructions provided')}
"""
``

## 实现工具执行
工具执行处理程序负责实际执行每个工具的逻辑。让我们添加它：
``
@mcp.tool()
async def get_alerts(state: str) -> str:
    """Get weather alerts for a US state.

    Args:
        state: Two-letter US state code (e.g. CA, NY)
    """
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url)

    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."

    if not data["features"]:
        return "No active alerts for this state."

    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)

@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """Get weather forecast for a location.

    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    """
    # First get the forecast grid endpoint
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_nws_request(points_url)

    if not points_data:
        return "Unable to fetch forecast data for this location."

    # Get the forecast URL from the points response
    forecast_url = points_data["properties"]["forecast"]
    forecast_data = await make_nws_request(forecast_url)

    if not forecast_data:
        return "Unable to fetch detailed forecast."

    # Format the periods into a readable forecast
    periods = forecast_data["properties"]["periods"]
    forecasts = []
    for period in periods[:5]:  # Only show next 5 periods
        forecast = f"""
{period['name']}:
Temperature: {period['temperature']}°{period['temperatureUnit']}
Wind: {period['windSpeed']} {period['windDirection']}
Forecast: {period['detailedForecast']}
"""
        forecasts.append(forecast)

    return "\n---\n".join(forecasts)
``

## 运行服务器
最后，让我们初始化并运行服务器：
``
if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
``


您需要在密钥中添加服务器mcpServers。只有至少一台服务器正确配置后，MCP UI 元素才会显示在 Claude for Desktop 中。
在这种情况下，我们将像这样添加单个天气服务器：
``
{
  "mcpServers": {
    "weather": {
      "command": "uv",
      "args": [
        "--directory",
        "/ABSOLUTE/PATH/TO/PARENT/FOLDER/weather",
        "run",
        "weather.py"
      ]
    }
  }
}
``

uv您可能需要在字段中输入可执行文件的完整路径command。您可以通过which uv在 macOS/Linux 或where uvWindows 上运行来获取此信息。

确保传入服务器的绝对路径。您可以pwd在 macOS/Linux 或Windows 命令提示符下运行此命令。在 Windows 上，请记住在 JSON 路径中cd使用双反斜杠 ( \\) 或正斜杠 ( )。/

这告诉 Claude for Desktop：
有一个名为“天气”的 MCP 服务器
通过运行来启动它uv --directory /ABSOLUTE/PATH/TO/PARENT/FOLDER/weather run weather.py
保存文件，然后重新启动Claude for Desktop。

# 幕后发生了什么
当你问一个问题时：
1. client将您的问题发送给 大模型
2. 大模型 分析可用的工具并决定使用哪一个
3. 客户端通过 MCP 服务器执行所选工具
4. 结果发回给大模型
5. 大模型通过自然语言进行回应
6. 答案已显示给您！