# MCP天气服务器快速入门

在本教程中，我们将构建一个简单的MCP天气服务器，并将其连接到主机Claude for Desktop。我们将从基本设置开始，然后逐步进展到更复杂的用例。

## 我们将构建的内容

许多大型语言模型（LLMs）目前无法获取天气预报和严重天气警报。让我们使用MCP来解决这个问题！我们将构建一个服务器，提供两个工具：`get_alerts`和`get_forecast`，然后将服务器连接到MCP主机（在本例中为Claude for Desktop）。

## 核心MCP概念

MCP服务器可以提供三种主要类型的功能：

1. **资源**：可以被客户端读取的文件类数据（如API响应或文件内容）
2. **工具**：可以被LLM调用的函数（需用户批准）
3. **提示**：帮助用户完成特定任务的预写模板

本教程将主要关注工具。

## 系统要求

- 安装Python 3.10或更高版本。
- 必须使用Python MCP SDK 1.2.0或更高版本。

## 设置环境

首先，安装`uv`并设置Python项目和环境。

## 构建服务器

### 导入包并设置实例

在`weather.py`的顶部添加以下内容：

```python
from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# 初始化FastMCP服务器
mcp = FastMCP("weather")
```

### 辅助函数

接下来，添加用于查询和格式化来自国家气象局API的数据的辅助函数。

### 实现工具执行

工具执行处理程序负责实际执行每个工具的逻辑。

## 完整代码

[您可以在这里找到我们将要构建的完整代码。](https://github.com/modelcontextprotocol/quickstart-resources/tree/main/weather-server-python)
