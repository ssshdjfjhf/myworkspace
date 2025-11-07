// API基础URL
const API_BASE = '/api';

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', () => {
  const urlParams = new URLSearchParams(window.location.search);
  const movieId = urlParams.get('id');

  if (movieId) {
    loadMovieDetail(movieId);
  } else {
    showError('电影ID不存在');
  }

  // 搜索框回车事件
  document.getElementById('searchInput').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
      searchMovies();
    }
  });
});

// 加载电影详情
async function loadMovieDetail(movieId) {
  try {
    const response = await fetch(`${API_BASE}/movies/${movieId}`);
    const result = await response.json();

    if (result.success) {
      renderMovieDetail(result.data);
      document.title = `${result.data.title} - 个人电影网`;
    } else {
      showError('电影不存在');
    }
  } catch (error) {
    console.error('加载电影详情失败:', error);
    showError('加载失败，请刷新页面重试');
  }
}

// 渲染电影详情
function renderMovieDetail(movie) {
  const container = document.getElementById('movieDetail');
  const ratingCount = formatNumber(movie.ratingCount);

  const html = `
    <div class="detail-header">
      <img src="${movie.poster}" alt="${movie.title}" class="detail-poster"
           onerror="this.src='https://via.placeholder.com/250x350?text=暂无海报'">

      <div class="detail-info">
        <h1 class="detail-title">${movie.title}</h1>
        <p class="detail-original-title">${movie.originalTitle}</p>

        <div class="detail-rating">
          <div class="detail-rating-score">${movie.rating}</div>
          <div class="detail-rating-info">
            <div>⭐⭐⭐⭐⭐</div>
            <div style="color: #999; font-size: 14px;">${ratingCount}人评价</div>
          </div>
        </div>

        <div class="detail-meta">
          <div class="detail-meta-item">
            <span class="detail-meta-label">导演:</span>
            <span>${movie.directors.join(' / ')}</span>
          </div>

          <div class="detail-meta-item">
            <span class="detail-meta-label">主演:</span>
            <span>${movie.actors.join(' / ')}</span>
          </div>

          <div class="detail-meta-item">
            <span class="detail-meta-label">类型:</span>
            <span>${movie.genres.join(' / ')}</span>
          </div>

          <div class="detail-meta-item">
            <span class="detail-meta-label">地区:</span>
            <span>${movie.regions.join(' / ')}</span>
          </div>

          <div class="detail-meta-item">
            <span class="detail-meta-label">年份:</span>
            <span>${movie.year}</span>
          </div>

          <div class="detail-meta-item">
            <span class="detail-meta-label">片长:</span>
            <span>${movie.duration}分钟</span>
          </div>

          ${movie.tags ? `
          <div class="detail-meta-item">
            <span class="detail-meta-label">标签:</span>
            <span>${movie.tags.map(tag => `<span class="movie-tag">${tag}</span>`).join(' ')}</span>
          </div>
          ` : ''}
        </div>
      </div>
    </div>

    <div class="detail-summary">
      <h2 class="detail-summary-title">剧情简介</h2>
      <p class="detail-summary-text">${movie.summary}</p>
    </div>
  `;

  container.innerHTML = html;
}

// 搜索电影
function searchMovies() {
  const searchInput = document.getElementById('searchInput');
  const keyword = searchInput.value.trim();

  if (!keyword) {
    alert('请输入搜索关键词');
    return;
  }

  // 跳转到首页并传递搜索参数
  window.location.href = `/?search=${encodeURIComponent(keyword)}`;
}

// 格式化数字
function formatNumber(num) {
  if (num >= 10000) {
    return (num / 10000).toFixed(1) + '万';
  }
  return num.toLocaleString();
}

// 显示错误
function showError(message) {
  const container = document.getElementById('movieDetail');
  container.innerHTML = `
    <div class="empty-state">
      <div class="empty-state-icon">⚠️</div>
      <p>${message}</p>
      <button class="filter-btn" onclick="window.location.href='/'">返回首页</button>
    </div>
  `;
}
