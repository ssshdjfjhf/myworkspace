const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 3000;

// 中间件
app.use(cors());
app.use(bodyParser.json());
app.use(express.static('public'));

// 读取电影数据
function getMoviesData() {
  const data = fs.readFileSync(path.join(__dirname, 'data', 'movies.json'), 'utf8');
  return JSON.parse(data);
}

// API路由

// 获取所有电影
app.get('/api/movies', (req, res) => {
  try {
    const data = getMoviesData();
    const { genre, region, sort, search } = req.query;

    let movies = data.movies;

    // 搜索过滤
    if (search) {
      const searchLower = search.toLowerCase();
      movies = movies.filter(movie =>
        movie.title.toLowerCase().includes(searchLower) ||
        movie.originalTitle.toLowerCase().includes(searchLower) ||
        movie.directors.some(d => d.toLowerCase().includes(searchLower)) ||
        movie.actors.some(a => a.toLowerCase().includes(searchLower))
      );
    }

    // 类型过滤
    if (genre) {
      movies = movies.filter(movie => movie.genres.includes(genre));
    }

    // 地区过滤
    if (region) {
      movies = movies.filter(movie => movie.regions.includes(region));
    }

    // 排序
    if (sort === 'rating') {
      movies.sort((a, b) => b.rating - a.rating);
    } else if (sort === 'year') {
      movies.sort((a, b) => b.year - a.year);
    } else if (sort === 'hot') {
      movies.sort((a, b) => b.ratingCount - a.ratingCount);
    }

    res.json({
      success: true,
      data: movies,
      total: movies.length
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: '获取电影列表失败',
      error: error.message
    });
  }
});

// 获取单个电影详情
app.get('/api/movies/:id', (req, res) => {
  try {
    const data = getMoviesData();
    const movie = data.movies.find(m => m.id === parseInt(req.params.id));

    if (movie) {
      res.json({
        success: true,
        data: movie
      });
    } else {
      res.status(404).json({
        success: false,
        message: '电影不存在'
      });
    }
  } catch (error) {
    res.status(500).json({
      success: false,
      message: '获取电影详情失败',
      error: error.message
    });
  }
});

// 获取正在热映
app.get('/api/movies/status/now-playing', (req, res) => {
  try {
    const data = getMoviesData();
    const nowPlayingMovies = data.movies.filter(m =>
      data.nowPlaying.includes(m.id)
    );

    res.json({
      success: true,
      data: nowPlayingMovies
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: '获取热映电影失败',
      error: error.message
    });
  }
});

// 获取即将上映
app.get('/api/movies/status/coming-soon', (req, res) => {
  try {
    const data = getMoviesData();
    const comingSoonMovies = data.movies.filter(m =>
      data.comingSoon.includes(m.id)
    );

    res.json({
      success: true,
      data: comingSoonMovies
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: '获取即将上映电影失败',
      error: error.message
    });
  }
});

// 获取高分电影
app.get('/api/movies/status/top-rated', (req, res) => {
  try {
    const data = getMoviesData();
    const topRatedMovies = data.movies.filter(m =>
      data.topRated.includes(m.id)
    );

    res.json({
      success: true,
      data: topRatedMovies
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: '获取高分电影失败',
      error: error.message
    });
  }
});

// 获取所有类型
app.get('/api/genres', (req, res) => {
  try {
    const data = getMoviesData();
    const genres = [...new Set(data.movies.flatMap(m => m.genres))];

    res.json({
      success: true,
      data: genres
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: '获取类型列表失败',
      error: error.message
    });
  }
});

// 获取所有地区
app.get('/api/regions', (req, res) => {
  try {
    const data = getMoviesData();
    const regions = [...new Set(data.movies.flatMap(m => m.regions))];

    res.json({
      success: true,
      data: regions
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: '获取地区列表失败',
      error: error.message
    });
  }
});

// 首页路由
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// 详情页路由
app.get('/detail/:id', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'detail.html'));
});

// 启动服务器
app.listen(PORT, () => {
  console.log(`
╔════════════════════════════════════════╗
║   🎬 电影网站服务器已启动              ║
║                                        ║
║   访问地址: http://localhost:${PORT}     ║
║   API文档: http://localhost:${PORT}/api ║
║                                        ║
║   按 Ctrl+C 停止服务器                 ║
╚════════════════════════════════════════╝
  `);
});
