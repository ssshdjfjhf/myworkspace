// API基础URL
const API_BASE = '/api';

// 当前筛选条件
let currentFilters = {
  genre: '',
  region: '',
  sort: 'rating'
};

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', () => {
  loadNowPlaying();
  loadComingSoon();
  loadTopRated();

  // 搜索框回车事件
  document.getElementById('searchInput').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
      searchMovies();
    }
  });
});

// 加载正在热映
async function loadNowPlaying() {
  try {
    const response = await fetch(`${API_BASE}/movies/status/now-playing`);
    const result = await response.json();

    if (result.success) {
      renderMovies(result.data, 'nowPlayingGrid');
    }
  } catch (error) {
    console.error('加载正在热映失败:', error);
    showError('nowPlayingGrid');
  }
}

// 加载即将上映
async function loadComingSoon() {
  try {
    const response = await fetch(`${API_BASE}/movies/status/coming-soon`);
    const result = await response.json();

    if (result.success) {
      renderMovies(result.data, 'comingSoonGrid');
    }
  } catch (error) {
    console.error('加载即将上映失败:', error);
    showError('comingSoonGrid');
  }
}

// 加载高分电影
async function loadTopRated() {
  try {
    const params = new URLSearchParams();
    if (currentFilters.genre) params.append('genre', currentFilters.genre);
    if (currentFilters.region) params.append('region', currentFilters.region);
    if (currentFilters.sort) params.append('sort', currentFilters.sort);

    const response = await fetch(`${API_BASE}/movies/status/top-rated?${params}`);
    const result = await response.json();

    if (result.success) {
      renderMovies(result.data, 'topRatedGrid');
    }
  } catch (error) {
    console.error('加载高分电影失败:', error);
    showError('topRatedGrid');
  }
}

// 加载所有电影
async function loadAllMovies() {
  try {
    const params = new URLSearchParams();
    if (currentFilters.genre) params.append('genre', currentFilters.genre);
    if (currentFilters.region) params.append('region', currentFilters.region);
    params.append('sort', 'rating');

    const response = await fetch(`${API_BASE}/movies?${params}`);
    const result = await response.json();

    if (result.success) {
      renderMovies(result.data, 'topRatedGrid');
      // 滚动到高分电影区域
      document.getElementById('top-rated').scrollIntoView({ behavior: 'smooth' });
    }
  } catch (error) {
    console.error('加载所有电影失败:', error);
  }
}

// 搜索电影
async function searchMovies() {
  const searchInput = document.getElementById('searchInput');
  const keyword = searchInput.value.trim();

  if (!keyword) {
    alert('请输入搜索关键词');
    return;
  }

  try {
    const response = await fetch(`${API_BASE}/movies?search=${encodeURIComponent(keyword)}`);
    const result = await response.json();

    if (result.success) {
      if (result.data.length === 0) {
        showEmpty('topRatedGrid', '没有找到相关电影');
      } else {
        renderMovies(result.data, 'topRatedGrid');
        // 滚动到结果区域
        document.getElementById('top-rated').scrollIntoView({ behavior: 'smooth' });
      }
    }
  } catch (error) {
    console.error('搜索失败:', error);
    alert('搜索失败，请稍后重试');
  }
}

// 按类型筛选
function filterByGenre(genre) {
  currentFilters.genre = genre;
  updateFilterButtons('genre', genre);
  loadTopRated();
}

// 按地区筛选
function filterByRegion(region) {
  currentFilters.region = region;
  updateFilterButtons('region', region);
  loadTopRated();
}

// 更新筛选按钮状态
function updateFilterButtons(type, value) {
  const filterGroups = document.querySelectorAll('.filter-group');
  filterGroups.forEach(group => {
    const buttons = group.querySelectorAll('.filter-btn');
    buttons.forEach(btn => {
      if (type === 'genre' && group.querySelector('.filter-label').textContent.includes('类型')) {
        btn.classList.remove('active');
        if ((value === '' && btn.textContent === '全部') ||
            (value !== '' && btn.textContent === value)) {
          btn.classList.add('active');
        }
      } else if (type === 'region' && group.querySelector('.filter-label').textContent.includes('地区')) {
        btn.classList.remove('active');
        if ((value === '' && btn.textContent === '全部') ||
            (value !== '' && btn.textContent === value)) {
          btn.classList.add('active');
        }
      }
    });
  });
}

// 渲染电影列表
function renderMovies(movies, containerId) {
  const container = document.getElementById(containerId);

  if (!movies || movies.length === 0) {
    showEmpty(containerId, '暂无电影数据');
    return;
  }

  const html = movies.map(movie => createMovieCard(movie)).join('');
  container.innerHTML = html;
}

// 创建电影卡片
function createMovieCard(movie) {
  const ratingCount = formatNumber(movie.ratingCount);

  return `
    <div class="movie-card" onclick="goToDetail(${movie.id})">
      <img src="${movie.poster}" alt="${movie.title}" class="movie-poster"
           onerror="this.src='https://via.placeholder.com/150x220?text=暂无海报'">
      <div class="movie-info">
        <div class="movie-title" title="${movie.title}">${movie.title}</div>
        <div class="movie-rating">
          <span class="rating-score">${movie.rating}</span>
          <span class="rating-count">(${ratingCount}人评价)</span>
        </div>
        <div class="movie-meta">
          ${movie.genres.slice(0, 2).map(g => `<span class="movie-tag">${g}</span>`).join('')}
        </div>
      </div>
    </div>
  `;
}

// 跳转到详情页
function goToDetail(movieId) {
  window.location.href = `/detail.html?id=${movieId}`;
}

// 格式化数字
function formatNumber(num) {
  if (num >= 10000) {
    return (num / 10000).toFixed(1) + '万';
  }
  return num.toLocaleString();
}

// 显示错误
function showError(containerId) {
  const container = document.getElementById(containerId);
  container.innerHTML = `
    <div class="empty-state">
      <div class="empty-state-icon">⚠️</div>
      <p>加载失败，请刷新页面重试</p>
    </div>
  `;
}

// 显示空状态
function showEmpty(containerId, message) {
  const container = document.getElementById(containerId);
  container.innerHTML = `
    <div class="empty-state">
      <div class="empty-state-icon">📭</div>
      <p>${message}</p>
    </div>
  `;
}
