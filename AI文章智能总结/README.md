# AI文章智能总结系统

基于美团Friday大模型的AI文章智能总结系统，能够对爬取的AI工具/项目文章进行专业分析和总结。

## 🚀 功能特点

- **智能总结**: 使用美团Friday大模型对文章进行深度分析
- **结构化输出**: 按照固定格式输出核心功能、特点、应用场景等
- **批量处理**: 支持批量处理多篇文章，自动控制请求频率
- **多格式输出**: 生成JSON数据文件和Markdown报告
- **错误处理**: 完善的重试机制和异常处理
- **进度跟踪**: 实时显示处理进度和日志记录

## 📋 系统要求

- Python 3.7+
- requests库
- 美团Friday API访问权限

## 🛠️ 安装依赖

```bash
pip install requests
```

## ⚙️ 配置说明

### 1. API配置
在 `config.py` 中修改你的AppID：
```python
FRIDAY_CONFIG = {
    "app_id": "你的AppID",  # 替换为你的实际AppID
    # 其他配置...
}
```

### 2. 数据文件配置
指定输入的爬虫数据文件路径：
```python
DATA_CONFIG = {
    "input_file": "../爬取AI咨询/ai_articles_20250814_201716.json",
    # 其他配置...
}
```

### 3. 处理参数配置
调整批处理和延迟参数：
```python
PROCESS_CONFIG = {
    "batch_size": 3,    # 批处理大小，建议3-5
    "delay": 3.0,       # 批次间延迟（秒）
    "base_delay": 0.5,  # 基础延迟（秒）
    "max_retries": 3    # 最大重试次数
}
```

## 🎯 提示词设计

系统使用专业的提示词模板，对每篇文章进行结构化分析：

### 分析维度
- **🎯 核心功能**: 概括工具的核心功能和价值
- **🔧 主要特点**: 列出3-5个主要特点或亮点
- **🏷️ 应用场景**: 描述适用场景和目标用户
- **💡 创新点**: 指出相比同类产品的优势
- **📊 实用性评估**: 从技术成熟度、易用性等角度评估

### 输出要求
- 专业准确，突出技术特点
- 简洁明了，每部分控制在50字以内
- 客观中性，避免过度营销语言
- 突出实用价值和应用前景

## 🚀 使用方法

### 方法1: 直接运行
```bash
cd AI文章智能总结
python ai_article_summarizer.py
```

### 方法2: 作为模块使用
```python
from ai_article_summarizer import ArticleSummarizer

# 创建总结器
summarizer = ArticleSummarizer("你的AppID")

# 运行总结
articles = summarizer.run(
    input_file="path/to/articles.json",
    batch_size=3,
    delay=3.0
)
```

## 📊 输出文件

运行完成后会生成以下文件：

### 1. JSON数据文件
- 文件名: `summarized_articles_YYYYMMDD_HHMMSS.json`
- 内容: 包含原始数据和AI总结的完整JSON数据

### 2. Markdown报告
- 文件名: `summary_report_YYYYMMDD_HHMMSS.md`
- 内容: 格式化的总结报告，包含统计信息和详细总结

### 3. 日志文件
- 文件名: `ai_summarizer.log`
- 内容: 详细的运行日志和错误信息

## 📈 处理流程

1. **加载数据**: 从JSON文件加载爬虫数据
2. **批量处理**: 按批次处理文章，避免API限流
3. **智能总结**: 调用Friday API生成结构化总结
4. **保存结果**: 保存JSON数据和Markdown报告
5. **生成统计**: 统计处理结果和分类信息

## ⚠️ 注意事项

### API使用
- 确保AppID有效且有足够的API调用额度
- 建议设置合理的批处理大小和延迟时间
- 注意API的并发限制和频率限制

### 数据处理
- 输入文件必须是有效的JSON格式
- 确保文章数据包含必要的字段（title, description等）
- 处理大量文章时建议分批进行

### 错误处理
- 系统会自动重试失败的请求
- 失败的文章会标记为"总结生成失败"
- 查看日志文件了解详细错误信息

## 🔧 自定义配置

### 修改提示词
在 `ai_article_summarizer.py` 的 `create_summary_prompt` 方法中修改提示词模板。

### 调整输出格式
在 `generate_summary_report` 方法中修改报告格式。

### 添加新的分析维度
在提示词中添加新的分析部分，如技术栈、竞品对比等。

## 📞 技术支持

如遇到问题，请检查：
1. AppID是否正确配置
2. 输入文件路径是否存在
3. 网络连接是否正常
4. API调用额度是否充足

查看 `ai_summarizer.log` 文件获取详细错误信息。
