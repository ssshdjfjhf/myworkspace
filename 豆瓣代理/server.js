const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const axios = require('axios');
const cheerio = require('cheerio');

const app = express();
const PORT = 3000;

// 豆瓣目标地址
const DOUBAN_TARGET = 'https://movie.douban.com';

// 静态文件服务
app.use('/custom', express.static('public'));

// 图片代理路由 - 解决防盗链问题
app.get('/proxy-image', async (req, res) => {
  try {
    const imageUrl = req.query.url;
    if (!imageUrl) {
      return res.status(400).send('Missing image URL');
    }

    const response = await axios.get(imageUrl, {
      responseType: 'arraybuffer',
      headers: {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://movie.douban.com/',
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8'
      },
      timeout: 10000
    });

    // 设置正确的 Content-Type
    const contentType = response.headers['content-type'] || 'image/jpeg';
    res.set('Content-Type', contentType);
    res.set('Cache-Control', 'public, max-age=86400'); // 缓存1天
    res.send(response.data);
  } catch (error) {
    console.error('图片代理错误:', error.message);
    res.status(500).send('Image proxy error');
  }
});

// 努努影院搜索解析API
app.get('/api/parse-nunuyy', async (req, res) => {
  try {
    const movieTitle = req.query.title;
    if (!movieTitle) {
      return res.status(400).json({ error: 'Missing movie title' });
    }

    console.log(`解析努努影院: ${movieTitle}`);

    // 请求努努影院搜索页面
    const searchUrl = `https://nnyy.in/so?q=${encodeURIComponent(movieTitle)}`;
    const response = await axios.get(searchUrl, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9',
      },
      timeout: 10000
    });

    // 使用 cheerio 解析HTML
    const $ = cheerio.load(response.data);

    // 查找第一个搜索结果的链接
    // 根据你提供的HTML结构: <a href="/dianying/20259243.html">
    let videoUrl = null;

    // 尝试多种选择器来找到视频链接
    const selectors = [
      'a[href*="/dianying/"]',
      'a[href*="/dianshiju/"]',
      'a[href*="/zongyi/"]',
      'a[href*="/dongman/"]',
      '.lists-content a',
      '.thumbnail a',
      'li a'
    ];

    for (const selector of selectors) {
      // 遍历所有匹配的链接,找到第一个包含.html的完整链接
      $(selector).each((i, elem) => {
        if (videoUrl) return false; // 如果已找到,跳出循环

        const href = $(elem).attr('href');
        console.log(`检查链接 [${selector}]:`, href);

        // 必须包含.html且不是根目录
        if (href && href.includes('.html') && href.length > 15) {
          // 确保链接格式正确: /dianying/20259243.html
          if (href.match(/\/(dianying|dianshiju|zongyi|dongman)\/\d+\.html/)) {
            videoUrl = href.startsWith('http') ? href : `https://nnyy.in${href}`;
            console.log(`✅ 找到有效视频链接: ${videoUrl}`);
            return false; // 跳出each循环
          }
        }
      });

      if (videoUrl) break; // 如果已找到,跳出for循环
    }

    if (videoUrl) {
      res.json({
        success: true,
        url: videoUrl,
        title: movieTitle
      });
    } else {
      // 如果没找到,返回搜索页面
      res.json({
        success: false,
        url: searchUrl,
        message: '未找到直接播放链接,返回搜索页面'
      });
    }

  } catch (error) {
    console.error('努努影院解析错误:', error.message);
    res.status(500).json({
      success: false,
      error: error.message,
      url: `https://nnyy.in/so?q=${encodeURIComponent(req.query.title || '')}`
    });
  }
});

// 自定义路由 - 在这里可以注入自定义内容
app.get('*', async (req, res) => {
  try {
    // 处理豆瓣的link2跳转链接
    if (req.path.startsWith('/link2/')) {
      // 提取真实的URL
      const realUrl = req.query.url;
      if (realUrl) {
        try {
          const url = new URL(realUrl);
          // 如果是豆瓣域名,转换为相对路径并重定向
          if (url.hostname.includes('douban.com')) {
            const redirectPath = url.pathname + url.search + url.hash;
            console.log(`link2跳转: ${realUrl} -> ${redirectPath}`);
            return res.redirect(redirectPath);
          }
        } catch (e) {
          console.error('解析link2 URL失败:', e.message);
        }
      }
      // 如果解析失败,返回404
      return res.status(404).send('Invalid link2 URL');
    }

    // 判断是否是搜索请求
    let targetUrl;
    if (req.path.startsWith('/search') || req.query.search_text) {
      // 搜索请求转换为豆瓣主站搜索格式
      const searchText = req.query.search_text || req.query.q || '';
      targetUrl = `https://www.douban.com/search?q=${encodeURIComponent(searchText)}&cat=1002`;
    } else {
      // 其他请求使用 movie.douban.com
      targetUrl = `${DOUBAN_TARGET}${req.path}${req.url.includes('?') ? req.url.substring(req.url.indexOf('?')) : ''}`;
    }

    console.log(`代理请求: ${targetUrl}`);

    // 请求豆瓣页面
    const response = await axios.get(targetUrl, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Referer': targetUrl.includes('www.douban.com') ? 'https://www.douban.com/' : 'https://movie.douban.com/'
      },
      timeout: 10000,
      maxRedirects: 5
    });

    let html = response.data;

    // 使用 cheerio 解析和修改 HTML
    const $ = cheerio.load(html);

    // 修改所有链接,确保豆瓣链接通过代理访问
    $('a').each((i, elem) => {
      const href = $(elem).attr('href');
      if (!href) return;

      // 相对路径 - 保持不变,会自动通过代理
      if (href.startsWith('/') && !href.startsWith('//')) {
        // 相对路径已经是正确的,不需要修改
        // 例如: /subject/123/ 会自动访问 localhost:3000/subject/123/
      }
      // 协议相对路径 - 转换为相对路径
      else if (href.startsWith('//')) {
        const url = new URL('https:' + href);
        // 如果是豆瓣域名,转换为相对路径
        if (url.hostname.includes('douban.com')) {
          $(elem).attr('href', url.pathname + url.search + url.hash);
        }
        // 否则保持原样(外部链接)
      }
      // 绝对路径 - 处理豆瓣链接
      else if (href.startsWith('http')) {
        try {
          const url = new URL(href);
          // 如果是豆瓣域名,转换为相对路径通过代理访问
          if (url.hostname.includes('douban.com')) {
            $(elem).attr('href', url.pathname + url.search + url.hash);
          }
          // 外部链接保持不变,并添加新窗口打开
          else {
            $(elem).attr('target', '_blank');
            $(elem).attr('rel', 'noopener noreferrer');
          }
        } catch (e) {
          // URL解析失败,保持原样
        }
      }
    });

    // 修改图片链接 - 通过代理服务器加载以解决防盗链
    // 根据当前请求的域名来确定图片的基础URL
    const imageBaseUrl = targetUrl.includes('www.douban.com') ? 'https://www.douban.com' : DOUBAN_TARGET;

    $('img').each((i, elem) => {
      // 处理 src 属性
      const src = $(elem).attr('src');
      if (src) {
        let fullUrl = src;
        if (src.startsWith('//')) {
          fullUrl = 'https:' + src;
        } else if (src.startsWith('/')) {
          fullUrl = imageBaseUrl + src;
        }
        // 通过我们的代理服务器加载图片
        if (fullUrl.startsWith('http')) {
          $(elem).attr('src', `/proxy-image?url=${encodeURIComponent(fullUrl)}`);
        }
      }

      // 处理懒加载的 data-src 属性
      const dataSrc = $(elem).attr('data-src');
      if (dataSrc) {
        let fullUrl = dataSrc;
        if (dataSrc.startsWith('//')) {
          fullUrl = 'https:' + dataSrc;
        } else if (dataSrc.startsWith('/')) {
          fullUrl = imageBaseUrl + dataSrc;
        }
        if (fullUrl.startsWith('http')) {
          $(elem).attr('data-src', `/proxy-image?url=${encodeURIComponent(fullUrl)}`);
          // 同时设置 src 以立即加载
          $(elem).attr('src', `/proxy-image?url=${encodeURIComponent(fullUrl)}`);
        }
      }
    });

    // 修改CSS和JS链接
    $('link[rel="stylesheet"]').each((i, elem) => {
      const href = $(elem).attr('href');
      if (href && href.startsWith('//')) {
        $(elem).attr('href', 'https:' + href);
      } else if (href && href.startsWith('/')) {
        $(elem).attr('href', DOUBAN_TARGET + href);
      }
    });

    $('script').each((i, elem) => {
      const src = $(elem).attr('src');
      if (src && src.startsWith('//')) {
        $(elem).attr('src', 'https:' + src);
      } else if (src && src.startsWith('/')) {
        $(elem).attr('src', DOUBAN_TARGET + src);
      }
    });

    // 修改表单action,确保提交也通过代理
    $('form').each((i, elem) => {
      const action = $(elem).attr('action');
      if (action) {
        if (action.startsWith('http')) {
          try {
            const url = new URL(action);
            if (url.hostname.includes('douban.com')) {
              $(elem).attr('action', url.pathname + url.search);
            }
          } catch (e) {
            // 忽略解析错误
          }
        }
        // 相对路径保持不变
      }
    });

    // 处理可能包含跳转的meta标签
    $('meta[http-equiv="refresh"]').each((i, elem) => {
      const content = $(elem).attr('content');
      if (content && content.includes('url=')) {
        const newContent = content.replace(/url=https?:\/\/[^\/]*douban\.com/gi, 'url=');
        $(elem).attr('content', newContent);
      }
    });

    // 在每个电影项目中注入自定义下载按钮
    // 这里以电影列表项为例
    $('.item').each((i, elem) => {
      const movieId = $(elem).find('a').attr('href');
      if (movieId) {
        // 在电影信息后添加自定义下载按钮
        $(elem).append(`
          <div class="custom-download-btn" style="margin-top: 10px;">
            <a href="/download?movie=${encodeURIComponent(movieId)}"
               style="background: #42bd56; color: white; padding: 5px 15px;
                      border-radius: 3px; text-decoration: none; display: inline-block;">
              📥 下载资源
            </a>
          </div>
        `);
      }
    });

    // 获取当前页面的电影ID(如果是详情页)
    const currentMovieId = req.path.match(/\/subject\/(\d+)/)?.[1] || '';
    const currentMovieTitle = $('h1 span').first().text() || $('title').text();

    // 只在电影详情页注入自定义功能窗口
    if (currentMovieId) {
      $('body').append(`
        <style>
          .custom-download-section {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: #fff;
            border: 2px solid #42bd56;
            border-radius: 8px;
            padding: 15px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            z-index: 99999 !important;
            min-width: 200px;
          }
          .custom-download-section h3 {
            margin: 0 0 10px 0;
            color: #42bd56;
            font-size: 16px;
            font-weight: bold;
          }
          .custom-download-btn-main {
            background: #42bd56;
            color: white;
            padding: 10px 20px;
            border-radius: 4px;
            text-decoration: none;
            display: block;
            cursor: pointer;
            border: none;
            font-size: 14px;
            width: 100%;
            text-align: center;
            margin-bottom: 8px;
          }
          .custom-download-btn-main:hover {
            background: #3aa047;
          }
          .custom-close-btn {
            position: absolute;
            top: 5px;
            right: 8px;
            background: none;
            border: none;
            font-size: 18px;
            cursor: pointer;
            color: #999;
            padding: 0;
            line-height: 1;
          }
          .custom-close-btn:hover {
            color: #333;
          }
          .custom-movie-info {
            font-size: 12px;
            color: #666;
            margin-bottom: 10px;
            padding: 8px;
            background: #f5f5f5;
            border-radius: 4px;
            word-break: break-all;
          }

          /* 播放源选择弹窗样式 */
          .player-modal-overlay {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.7);
            z-index: 999999;
            justify-content: center;
            align-items: center;
          }
          .player-modal-overlay.active {
            display: flex;
          }
          .player-modal {
            background: white;
            border-radius: 12px;
            padding: 30px;
            max-width: 500px;
            width: 90%;
            max-height: 80vh;
            overflow-y: auto;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            animation: modalSlideIn 0.3s ease-out;
          }
          @keyframes modalSlideIn {
            from {
              transform: translateY(-50px);
              opacity: 0;
            }
            to {
              transform: translateY(0);
              opacity: 1;
            }
          }
          .player-modal h2 {
            margin: 0 0 20px 0;
            color: #333;
            font-size: 24px;
            text-align: center;
          }
          .player-modal-close {
            position: absolute;
            top: 15px;
            right: 15px;
            background: none;
            border: none;
            font-size: 28px;
            cursor: pointer;
            color: #999;
            line-height: 1;
            padding: 0;
            width: 30px;
            height: 30px;
          }
          .player-modal-close:hover {
            color: #333;
          }
          .player-source-list {
            display: grid;
            gap: 12px;
          }
          .player-source-item {
            display: flex;
            align-items: center;
            padding: 15px 20px;
            background: #f8f9fa;
            border: 2px solid #e9ecef;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s;
          }
          .player-source-item:hover {
            background: #e8f5e9;
            border-color: #42bd56;
            transform: translateX(5px);
          }
          .player-source-icon {
            font-size: 24px;
            margin-right: 15px;
          }
          .player-source-info {
            flex: 1;
          }
          .player-source-name {
            font-size: 16px;
            font-weight: bold;
            color: #333;
            margin-bottom: 4px;
          }
          .player-source-desc {
            font-size: 12px;
            color: #666;
          }
          .player-source-arrow {
            font-size: 20px;
            color: #999;
          }
          .player-modal-footer {
            margin-top: 20px;
            padding-top: 20px;
            border-top: 1px solid #e9ecef;
            text-align: center;
            color: #666;
            font-size: 12px;
          }
        </style>

        <div class="custom-download-section" id="customDownloadSection">
          <button class="custom-close-btn" onclick="document.getElementById('customDownloadSection').style.display='none'">×</button>
          <h3>🎬 自定义功能</h3>
          <div class="custom-movie-info">
            <strong>当前影片:</strong><br>
            ${currentMovieTitle}<br>
            <small>ID: ${currentMovieId}</small>
          </div>
          <button class="custom-download-btn-main" onclick="showPlayerSourceModal('${currentMovieId}', '${currentMovieTitle.replace(/'/g, "\\'")}')">
            📥 在线观看
          </button>
          <button class="custom-download-btn-main" onclick="downloadPageResources()">
            💾 下载当前页面资源
          </button>
          <button class="custom-download-btn-main" onclick="showCustomFeatures()">
            ⚙️ 更多功能
          </button>
        </div>

        <!-- 播放源选择弹窗 -->
        <div class="player-modal-overlay" id="playerModalOverlay" onclick="closePlayerModal(event)">
          <div class="player-modal" onclick="event.stopPropagation()">
            <h2>🎬 选择播放源</h2>
            <div class="player-source-list">
              <div class="player-source-item" onclick="playMovie('youtube', '${currentMovieId}', '${currentMovieTitle.replace(/'/g, "\\'")}')">
                <div class="player-source-icon">🎥</div>
                <div class="player-source-info">
                  <div class="player-source-name">YouTube</div>
                  <div class="player-source-desc">高清画质 · 国际平台</div>
                </div>
                <div class="player-source-arrow">→</div>
              </div>

              <div class="player-source-item" onclick="playMovie('nunuyy', '${currentMovieId}', '${currentMovieTitle.replace(/'/g, "\\'")}')">
                <div class="player-source-icon">🎬</div>
                <div class="player-source-info">
                  <div class="player-source-name">努努影院</div>
                  <div class="player-source-desc">免费在线 · 更新快速</div>
                </div>
                <div class="player-source-arrow">→</div>
              </div>

              <div class="player-source-item" onclick="playMovie('dytt', '${currentMovieId}', '${currentMovieTitle.replace(/'/g, "\\'")}')">
                <div class="player-source-icon">🌟</div>
                <div class="player-source-info">
                  <div class="player-source-name">电影天堂</div>
                  <div class="player-source-desc">经典资源 · 下载观看</div>
                </div>
                <div class="player-source-arrow">→</div>
              </div>

              <div class="player-source-item" onclick="playMovie('xunlei', '${currentMovieId}', '${currentMovieTitle.replace(/'/g, "\\'")}')">
                <div class="player-source-icon">⚡</div>
                <div class="player-source-info">
                  <div class="player-source-name">迅雷资源</div>
                  <div class="player-source-desc">高速下载 · 蓝光画质</div>
                </div>
                <div class="player-source-arrow">→</div>
              </div>

              <div class="player-source-item" onclick="playMovie('meituan', '${currentMovieId}', '${currentMovieTitle.replace(/'/g, "\\'")}')">
                <div class="player-source-icon">🍿</div>
                <div class="player-source-info">
                  <div class="player-source-name">美团观看</div>
                  <div class="player-source-desc">正版授权 · 会员专享</div>
                </div>
                <div class="player-source-arrow">→</div>
              </div>
            </div>

            <div class="player-modal-footer">
              💡 提示: 选择播放源后将跳转到对应平台观看
            </div>
          </div>
        </div>

        <script>
          // 自定义JavaScript功能
          console.log('豆瓣代理页面已加载 - 电影详情页');
          console.log('当前电影ID:', '${currentMovieId}');
          console.log('当前电影标题:', '${currentMovieTitle}');

          // 显示播放源选择弹窗
          function showPlayerSourceModal(movieId, movieTitle) {
            console.log('显示播放源选择:', movieId, movieTitle);
            const modal = document.getElementById('playerModalOverlay');
            if (modal) {
              modal.classList.add('active');
              document.body.style.overflow = 'hidden'; // 禁止背景滚动
            }
          }

          // 关闭播放源选择弹窗
          function closePlayerModal(event) {
            // 只有点击遮罩层时才关闭
            if (event.target.id === 'playerModalOverlay') {
              const modal = document.getElementById('playerModalOverlay');
              if (modal) {
                modal.classList.remove('active');
                document.body.style.overflow = ''; // 恢复滚动
              }
            }
          }

          // 播放电影
          async function playMovie(source, movieId, movieTitle) {
            console.log('选择播放源:', source, movieId, movieTitle);

            // 关闭弹窗
            const modal = document.getElementById('playerModalOverlay');
            if (modal) {
              modal.classList.remove('active');
              document.body.style.overflow = '';
            }

            // 努努影院需要先解析
            if (source === 'nunuyy') {
              try {
                // 显示加载提示
                console.log('正在解析努努影院链接...');

                // 调用后端API解析
                const response = await fetch('/api/parse-nunuyy?title=' + encodeURIComponent(movieTitle));
                const data = await response.json();

                if (data.success && data.url) {
                  console.log('解析成功,跳转到:', data.url);
                  window.open(data.url, '_blank');
                } else {
                  console.log('未找到直接播放链接,跳转到搜索页面');
                  window.open(data.url || 'https://nnyy.in/so?q=' + encodeURIComponent(movieTitle), '_blank');
                }
              } catch (error) {
                console.error('解析努努影院失败:', error);
                alert('解析失败,将跳转到搜索页面');
                window.open('https://nnyy.in/so?q=' + encodeURIComponent(movieTitle), '_blank');
              }
              return;
            }

            // 其他播放源直接跳转
            let url = '';
            switch(source) {
              case 'youtube':
                // YouTube搜索
                url = 'https://www.youtube.com/results?search_query=' + encodeURIComponent(movieTitle);
                break;
              case 'dytt':
                // 电影天堂搜索
                url = 'https://www.dy2018.com/e/search/result/?searchid=' + encodeURIComponent(movieTitle);
                break;
              case 'xunlei':
                // 迅雷资源搜索
                url = 'https://www.xunleige.com/search?keyword=' + encodeURIComponent(movieTitle);
                break;
              case 'meituan':
                // 美团电影搜索
                url = 'https://maoyan.com/films?keyword=' + encodeURIComponent(movieTitle);
                break;
              default:
                alert('未知的播放源');
                return;
            }

            // 在新窗口打开
            window.open(url, '_blank');
          }

          // 下载页面资源
          function downloadPageResources() {
            const currentUrl = window.location.pathname + window.location.search;
            window.open('/download?page=' + encodeURIComponent(currentUrl), '_blank');
          }

          // 显示更多功能
          function showCustomFeatures() {
            alert('更多自定义功能开发中...\\n\\n可以添加:\\n- 批量下载\\n- 收藏管理\\n- 评分统计\\n- 资源搜索等');
          }

          // 页面加载完成
          document.addEventListener('DOMContentLoaded', function() {
            console.log('电影详情页加载完成,自定义功能已激活');

            // 确保浮动窗口在最上层
            const section = document.getElementById('customDownloadSection');
            if (section) {
              section.style.zIndex = '99999';
            }
          });

          // 可以通过快捷键显示/隐藏浮动窗口
          document.addEventListener('keydown', function(e) {
            // Ctrl/Cmd + Shift + D 切换显示
            if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'D') {
              const section = document.getElementById('customDownloadSection');
              if (section) {
                section.style.display = section.style.display === 'none' ? 'block' : 'none';
              }
            }
          });
        </script>
      `);
    } else {
      // 在非详情页只注入基础的日志脚本
      $('body').append(`
        <script>
          console.log('豆瓣代理页面已加载 - 非详情页');
          console.log('当前页面路径:', window.location.pathname);
        </script>
      `);
    }

    // 返回修改后的HTML
    res.send($.html());

  } catch (error) {
    console.error('代理错误:', error.message);
    console.error('错误详情:', error.response?.status, error.response?.statusText);
    console.error('请求URL:', error.config?.url);
    res.status(500).send(`
      <html>
        <head><title>代理错误</title></head>
        <body>
          <h1>代理请求失败</h1>
          <p>错误信息: ${error.message}</p>
          <p>状态码: ${error.response?.status || 'N/A'}</p>
          <p>请求URL: ${error.config?.url || 'N/A'}</p>
          <p>请检查网络连接或稍后重试</p>
        </body>
      </html>
    `);
  }
});

// 自定义下载路由
app.get('/download', (req, res) => {
  const movieId = req.query.movie;
  const movieTitle = req.query.title || '未知影片';
  const pageUrl = req.query.page;

  res.send(`
    <html>
      <head>
        <title>下载资源 - ${movieTitle}</title>
        <meta charset="utf-8">
        <style>
          body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            padding: 40px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            margin: 0;
          }
          .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            padding: 40px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
          }
          h1 {
            color: #333;
            margin-bottom: 10px;
          }
          .movie-title {
            color: #42bd56;
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 20px;
          }
          .info-box {
            background: #f5f5f5;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
          }
          .info-item {
            margin: 10px 0;
            padding: 10px;
            background: white;
            border-radius: 4px;
          }
          .info-label {
            font-weight: bold;
            color: #666;
            display: inline-block;
            width: 120px;
          }
          .download-section {
            margin: 30px 0;
            padding: 20px;
            background: #e8f5e9;
            border-radius: 8px;
            border-left: 4px solid #42bd56;
          }
          .download-link {
            display: block;
            padding: 15px 20px;
            background: #42bd56;
            color: white;
            text-decoration: none;
            border-radius: 6px;
            margin: 10px 0;
            text-align: center;
            transition: background 0.3s;
          }
          .download-link:hover {
            background: #3aa047;
          }
          .btn-back {
            padding: 12px 30px;
            background: #666;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 16px;
            transition: background 0.3s;
          }
          .btn-back:hover {
            background: #555;
          }
          .notice {
            background: #fff3cd;
            border: 1px solid #ffc107;
            padding: 15px;
            border-radius: 6px;
            margin: 20px 0;
            color: #856404;
          }
        </style>
      </head>
      <body>
        <div class="container">
          <h1>🎬 资源下载中心</h1>

          ${movieId ? `
            <div class="movie-title">${movieTitle}</div>

            <div class="info-box">
              <h3>📋 影片信息</h3>
              <div class="info-item">
                <span class="info-label">影片ID:</span>
                <span>${movieId}</span>
              </div>
              <div class="info-item">
                <span class="info-label">豆瓣链接:</span>
                <a href="https://movie.douban.com/subject/${movieId}/" target="_blank">
                  查看豆瓣页面
                </a>
              </div>
              <div class="info-item">
                <span class="info-label">代理链接:</span>
                <a href="/subject/${movieId}/" target="_blank">
                  在代理站查看
                </a>
              </div>
            </div>

            <div class="download-section">
              <h3>📥 下载选项</h3>
              <p>以下是可用的下载资源(示例):</p>
              <a href="#" class="download-link" onclick="alert('这里可以连接到实际的下载资源'); return false;">
                🎥 高清版本 (1080P)
              </a>
              <a href="#" class="download-link" onclick="alert('这里可以连接到实际的下载资源'); return false;">
                📱 移动版本 (720P)
              </a>
              <a href="#" class="download-link" onclick="alert('这里可以连接到实际的下载资源'); return false;">
                💿 蓝光原盘 (4K)
              </a>
            </div>
          ` : pageUrl ? `
            <div class="info-box">
              <h3>📄 页面资源</h3>
              <div class="info-item">
                <span class="info-label">页面路径:</span>
                <span>${pageUrl}</span>
              </div>
            </div>

            <div class="download-section">
              <h3>💾 页面资源下载</h3>
              <p>可以在这里添加页面截图、HTML保存等功能</p>
            </div>
          ` : `
            <div class="notice">
              ⚠️ 未指定下载内容
            </div>
          `}

          <div class="notice">
            <strong>💡 提示:</strong> 这是一个演示页面。实际使用时,你可以在这里:
            <ul>
              <li>连接到你的资源数据库</li>
              <li>提供磁力链接或下载地址</li>
              <li>添加用户认证和权限控制</li>
              <li>记录下载统计信息</li>
            </ul>
          </div>

          <button class="btn-back" onclick="history.back()">
            ← 返回上一页
          </button>
        </div>
      </body>
    </html>
  `);
});

app.listen(PORT, () => {
  console.log(`🚀 豆瓣代理服务器运行在 http://localhost:${PORT}`);
  console.log(`📝 访问 http://localhost:${PORT} 查看代理的豆瓣电影页面`);
});
