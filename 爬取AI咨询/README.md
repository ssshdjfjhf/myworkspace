# AI工具集网站爬虫

这个爬虫专门用于爬取 [AI工具集](https://ai-bot.cn/the-latest-ai-projects/) 网站的最新AI项目资讯。

## 功能特点

- 🎯 精确提取文章信息（标题、链接、描述、分类、发布时间等）
- 📊 支持多页面爬取
- 💾 支持JSON和CSV格式导出
- 🔄 智能重试机制
- 📝 详细的日志记录
- 🆕 识别新文章标记
- 🖼️ 提取文章配图链接

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 方法1：一键启动（推荐）

```bash
./run.sh
```

### 方法2：手动运行

首先创建虚拟环境并安装依赖：
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

然后运行爬虫：
```bash
python ai_news_scraper.py
```

### 自定义参数

在 `main()` 函数中可以修改以下参数：

- `MAX_PAGES`: 爬取页数（默认3页）
- `INCLUDE_CONTENT`: 是否获取文章详细内容（默认False，开启会显著增加时间）
- `SAVE_FORMATS`: 保存格式（默认['json', 'csv']）

## 输出文件

运行后会生成以下文件：

- `ai_articles_YYYYMMDD_HHMMSS.json`: JSON格式的文章数据
- `ai_articles_YYYYMMDD_HHMMSS.csv`: CSV格式的文章数据
- `scraper.log`: 爬取日志

## 数据字段说明

每篇文章包含以下字段：

- `title`: 文章标题
- `url`: 文章链接
- `description`: 文章描述
- `category`: 文章分类（如"AI工具"、"AI专栏"等）
- `publish_time`: 发布时间
- `image_url`: 配图链接
- `is_new`: 是否为新文章
- `scraped_at`: 爬取时间
- `content`: 文章详细内容（仅在开启时）

## 注意事项

1. 请合理控制爬取频率，避免对服务器造成压力
2. 建议在非高峰时段运行
3. 如需获取文章详细内容，请设置较小的页数以避免过长等待时间

## 示例输出

```
=== 爬取结果摘要 ===
总文章数: 30
新文章数: 8
分类统计:
  AI工具: 25篇
  AI专栏: 3篇
  AI教程: 2篇

=== 最新文章示例 ===

1. 🆕 BISHENG灵思 – 毕昇推出的开源通用AI Agent，基于AGL框架
   分类: AI工具
   时间: 4小时前
   链接: https://ai-bot.cn/bisheng-linsight/
   描述: BISHENG灵思是毕昇推出的开源通用AI Agent，通过结合业务专家的知识和经验...
