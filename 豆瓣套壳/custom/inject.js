// 自定义注入脚本

console.log('🔧 自定义脚本已加载');

// 等待DOM加载完成
document.addEventListener('DOMContentLoaded', function() {
  console.log('📄 页面加载完成,初始化自定义功能');

  // 为下载按钮添加点击事件
  const downloadButtons = document.querySelectorAll('.custom-download-btn');

  downloadButtons.forEach(button => {
    button.addEventListener('click', function() {
      const quality = this.getAttribute('data-quality');
      const movieTitle = document.querySelector('h1 span') ?
        document.querySelector('h1 span').textContent : '未知电影';

      // 这里可以自定义下载逻辑
      handleDownload(movieTitle, quality);
    });
  });

  // 添加自定义标记到标题
  const mainTitle = document.querySelector('#content h1');
  if (mainTitle && !mainTitle.querySelector('.custom-marker')) {
    const marker = document.createElement('span');
    marker.className = 'custom-marker';
    marker.textContent = '已增强';
    mainTitle.appendChild(marker);
  }
});

// 下载处理函数
function handleDownload(movieTitle, quality) {
  console.log(`准备下载: ${movieTitle} - ${quality}`);

  // 示例:显示提示信息
  const message = `
    电影: ${movieTitle}
    清晰度: ${quality}

    这是一个示例功能。
    在实际应用中,你可以:
    1. 跳转到你的下载页面
    2. 调用你的下载API
    3. 打开磁力链接
    4. 其他自定义操作
  `;

  alert(message);

  // 示例:跳转到自定义下载页面
  // window.open(`/download?movie=${encodeURIComponent(movieTitle)}&quality=${quality}`, '_blank');

  // 示例:调用自定义API
  // fetch('/api/download', {
  //   method: 'POST',
  //   headers: { 'Content-Type': 'application/json' },
  //   body: JSON.stringify({ movie: movieTitle, quality: quality })
  // });
}

// 添加键盘快捷键
document.addEventListener('keydown', function(e) {
  // Ctrl + D: 快速下载
  if (e.ctrlKey && e.key === 'd') {
    e.preventDefault();
    const firstDownloadBtn = document.querySelector('.custom-download-btn');
    if (firstDownloadBtn) {
      firstDownloadBtn.click();
    }
  }
});

// 监听页面变化(适用于SPA应用)
const observer = new MutationObserver(function(mutations) {
  // 可以在这里处理动态加载的内容
});

observer.observe(document.body, {
  childList: true,
  subtree: true
});
