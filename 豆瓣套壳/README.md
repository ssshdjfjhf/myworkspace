# 豆瓣电影代理网站

⚠️ **重要声明**: 本项目仅供个人学习和技术研究使用,请勿用于商业用途或公开部署。

## 项目简介

这是一个豆瓣电影的代理网站示例,演示了如何:
- 代理第三方网站内容
- 在页面中注入自定义元素
- 重写URL实现无缝浏览
- 添加自定义交互功能

## 功能特性

✅ 完整代理豆瓣电影网站内容
✅ 在电影详情页注入自定义下载按钮
✅ 支持自定义样式和脚本
✅ URL自动重写,保持浏览体验
✅ 可扩展的按钮点击处理逻辑

## 安装步骤

1. 安装依赖:
```bash
npm install
```

2. 启动服务器:
```bash
npm start
```

3. 访问网站:
```
http://localhost:3000
```

## 开发模式

使用 nodemon 自动重启:
```bash
npm run dev
```

## 自定义功能

### 添加自定义按钮

在 `server.js` 中的电影详情页部分,你可以添加更多按钮:

```javascript
<button class="custom-download-btn" data-quality="your-quality">
  你的按钮文字
</button>
```

### 自定义点击处理

在 `custom/inject.js` 中的 `handleDownload` 函数中实现你的逻辑:

```javascript
function handleDownload(movieTitle, quality) {
  // 你的自定义逻辑
  // 例如: 跳转到下载页面
  window.location.href = `/your-download-page?movie=${movieTitle}`;
}
```

### 修改样式

编辑 `custom/style.css` 来自定义按钮和页面样式。

## 技术栈

- **Node.js** - 运行环境
- **Express** - Web框架
- **Axios** - HTTP客户端
- **Cheerio** - HTML解析和操作

## 注意事项

1. **法律风险**: 未经授权代理他人网站可能违反服务条款和相关法律
2. **版权问题**: 展示他人内容需要获得授权
3. **仅供学习**: 本项目仅用于学习Web代理技术
4. **不要公开部署**: 请勿将此项目部署到公网

## 可能的问题

### 图片无法加载
豆瓣的图片可能有防盗链,这是正常现象。

### 某些功能不可用
由于是代理模式,一些依赖JavaScript的动态功能可能无法正常工作。

### 请求被拒绝
豆瓣可能会检测并拒绝代理请求,可以尝试调整User-Agent等请求头。

## 扩展建议

- 添加缓存机制提高性能
- 实现更智能的URL重写
- 添加用户认证系统
- 集成真实的下载资源API
- 添加搜索历史记录
- 实现收藏功能

## 许可证

MIT License - 仅供学习使用

---

**再次提醒**: 请遵守相关法律法规和网站服务条款,不要将此技术用于不当用途。
