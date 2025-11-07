const express = require('express');
const axios = require('axios');
const cheerio = require('cheerio');
const path = require('path');

const app = express();
const PORT = 3000;

// 豆瓣目标地址
const DOUBAN_BASE = 'https://movie.douban.com';

// 静态文件服务 - 用于自定义的CSS/JS
app.use('/custom', express.static(path.join(__dirname, 'custom')));

// 主代理路由
app.get('*', async (req, res) => {
  try {
    const targetUrl = DOUBAN_BASE + req.path + (req.url.includes('?') ? req.url.substring(req.url.indexOf('?')) : '');

    console.log(`代理请求: ${targetUrl}`);

    // 发起请求到豆瓣
    const response = await axios.get(targetUrl, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Referer': 'https://movie.douban.com/'
      },
      timeout: 10000,
      validateStatus: () => true // 接受所有状态码
    });

    const contentType = response.headers['content-type'] || '';

    // 如果是HTML内容,进行处理和注入
    if (contentType.includes('text/html')) {
      let html = response.data;

      // 使用cheerio解析HTML
      const $ = cheerio.load(html);

      // 重写所有URL,使其指向代理服务器
      $('a').each((i, elem) => {
        const href = $(elem).attr('href');
        if (href) {
          $(elem).attr('href', rewriteUrl(href));
        }
      });

      $('link').each((i, elem) => {
        const href = $(elem).attr('href');
        if (href) {
          $(elem).attr('href', rewriteUrl(href));
        }
      });

      $('script').each((i, elem) => {
        const src = $(elem).attr('src');
        if (src) {
          $(elem).attr('src', rewriteUrl(src));
        }
      });

      $('img').each((i, elem) => {
        const src = $(elem).attr('src');
        if (src) {
          $(elem).attr('data-original-src', src);
          // 保持豆瓣图片的原始链接
        }
      });

      // 注入自定义样式和脚本
      $('head').append(`
        <link rel="stylesheet" href="/custom/style.css">
        <script src="/custom/inject.js"></script>
      `);

      // 在电影详情页注入下载按钮
      if (req.path.includes('/subject/')) {
        // 在电影信息区域添加自定义按钮
        const movieInfo = $('#info');
        if (movieInfo.length > 0) {
          movieInfo.after(`
            <div class="custom-download-section" style="margin-top: 20px; padding: 15px; background: #f6f6f6; border-radius: 5px;">
              <h3 style="margin-bottom: 10px; color: #333;">📥 自定义下载链接</h3>
              <div class="custom-buttons">
                <button class="custom-download-btn" data-quality="1080p" style="margin: 5px; padding: 10px 20px; background: #00b51d; color: white; border: none; border-radius: 3px; cursor: pointer;">
                  高清下载 (1080P)
                </button>
                <button class="custom-download-btn" data-quality="720p" style="margin: 5px; padding: 10px 20px; background: #3ba0ff; color: white; border: none; border-radius: 3px; cursor: pointer;">
                  标清下载 (720P)
                </button>
                <button class="custom-download-btn" data-quality="4k" style="margin: 5px; padding: 10px 20px; background: #ff6a00; color: white; border: none; border-radius: 3px; cursor: pointer;">
                  超清下载 (4K)
                </button>
              </div>
              <p style="margin-top: 10px; font-size: 12px; color: #999;">
                ⚠️ 这是自定义注入的按钮示例,仅供学习使用
              </p>
            </div>
          `);
        }
      }

      // 添加页面底部提示
      $('body').append(`
        <div style="position: fixed; bottom: 10px; right: 10px; background: rgba(0,0,0,0.7); color: white; padding: 10px; border-radius: 5px; font-size: 12px; z-index: 9999;">
          🔧 代理模式 | 仅供学习
        </div>
      `);

      res.send($.html());
    } else {
      // 非HTML内容直接返回
      res.set(response.headers);
      res.status(response.status).send(response.data);
    }

  } catch (error) {
    console.error('代理错误:', error.message);
    res.status(500).send(`
      <html>
        <head><title>代理错误</title></head>
        <body>
          <h1>代理请求失败</h1>
          <p>错误信息: ${error.message}</p>
          <p>请检查网络连接或目标网站是否可访问</p>
          <a href="/">返回首页</a>
        </body>
      </html>
    `);
  }
});

// URL重写函数
function rewriteUrl(url) {
  if (!url) return url;

  // 跳过已经是完整URL的外部链接(非豆瓣域名)
  if (url.startsWith('http://') || url.startsWith('https://')) {
    if (url.includes('douban.com') || url.includes('doubanio.com')) {
      // 豆瓣相关域名,保持原样(图片等资源)
      return url;
    }
    return url;
  }

  // 相对路径转换为代理路径
  if (url.startsWith('/')) {
    return url;
  }

  return url;
}

app.listen(PORT, () => {
  console.log(`
╔════════════════════════════════════════════╗
║   豆瓣电影代理服务器已启动                 ║
║   访问地址: http://localhost:${PORT}        ║
║                                            ║
║   ⚠️  仅供个人学习使用                     ║
║   ⚠️  请勿用于商业或公开部署               ║
╚════════════════════════════════════════════╝
  `);
});
