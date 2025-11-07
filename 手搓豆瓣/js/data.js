/**
 * 数据管理模块
 * 负责加载和处理电影数据
 */

// 数据管理对象
const DataManager = {
    // 数据缓存
    cache: {
        nowPlaying: [],
        hotMovies: {},
        weeklyChart: [],
        hotLists: [],
        hotReviews: [],
        hotTV: {}
    },

    // 加载状态
    loadingStates: {
        nowPlaying: false,
        hotMovies: false,
        weeklyChart: false,
        hotLists: false,
        hotReviews: false,
        hotTV: false
    },

    // 错误状态
    errors: {},

    /**
     * 初始化数据管理器
     */
    init() {
        console.log('数据管理器初始化');
        return this;
    },

    /**
     * 加载JSON数据
     * @param {string} url - 数据文件路径
     * @returns {Promise} - 返回Promise对象
     */
    async loadJSON(url) {
        try {
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error(`加载数据失败: ${url}`, error);
            throw error;
        }
    },

    /**
     * 获取正在热映的电影
     * @returns {Promise<Array>} - 热映电影数组
     */
    async getNowPlayingMovies() {
        if (this.loadingStates.nowPlaying) {
            return this.cache.nowPlaying;
        }

        try {
            this.loadingStates.nowPlaying = true;
            const data = await this.loadJSON('data/movies.json');
            this.cache.nowPlaying = data.nowPlaying || [];
            return this.cache.nowPlaying;
        } catch (error) {
            this.errors.nowPlaying = error.message;
            console.error('获取热映电影失败:', error);
            // 抛出错误，以便上层可以捕获
            throw error;
        } finally {
            this.loadingStates.nowPlaying = false;
        }
    },

    /**
     * 获取热门电影
     * @param {string} category - 分类（hot, latest, highRated, hiddenGems）
     * @returns {Promise<Array>} - 热门电影数组
     */
    async getHotMovies(category = 'hot') {
        const cacheKey = `hotMovies_${category}`;

        if (this.cache.hotMovies[category]) {
            return this.cache.hotMovies[category];
        }

        try {
            const data = await this.loadJSON('data/movies.json');
            this.cache.hotMovies[category] = data.hotMovies[category] || [];
            return this.cache.hotMovies[category];
        } catch (error) {
            console.error(`获取${category}热门电影失败:`, error);
            return [];
        }
    },

    /**
     * 获取一周口碑榜
     * @returns {Promise<Array>} - 口碑榜数组
     */
    async getWeeklyChart() {
        if (this.cache.weeklyChart.length > 0) {
            return this.cache.weeklyChart;
        }

        try {
            const data = await this.loadJSON('data/movies.json');
            this.cache.weeklyChart = data.weeklyChart || [];
            return this.cache.weeklyChart;
        } catch (error) {
            console.error('获取口碑榜失败:', error);
            return [];
        }
    },

    /**
     * 获取热门片单
     * @returns {Promise<Array>} - 热门片单数组
     */
    async getHotLists() {
        if (this.cache.hotLists.length > 0) {
            return this.cache.hotLists;
        }

        try {
            const data = await this.loadJSON('data/movies.json');
            this.cache.hotLists = data.hotLists || [];
            return this.cache.hotLists;
        } catch (error) {
            console.error('获取热门片单失败:', error);
            return [];
        }
    },

    /**
     * 获取热门影评
     * @returns {Promise<Array>} - 热门影评数组
     */
    async getHotReviews() {
        if (this.cache.hotReviews.length > 0) {
            return this.cache.hotReviews;
        }

        try {
            const data = await this.loadJSON('data/movies.json');
            this.cache.hotReviews = data.hotReviews || [];
            return this.cache.hotReviews;
        } catch (error) {
            console.error('获取热门影评失败:', error);
            return [];
        }
    },

    /**
     * 获取热门电视剧
     * @param {string} category - 分类（all, cn, variety, us, jp, kr, animation, documentary）
     * @returns {Promise<Array>} - 热门电视剧数组
     */
    async getHotTV(category = 'all') {
        const cacheKey = `hotTV_${category}`;

        if (this.cache.hotTV[category]) {
            return this.cache.hotTV[category];
        }

        try {
            const data = await this.loadJSON('data/movies.json');
            this.cache.hotTV[category] = data.hotTV[category] || [];
            return this.cache.hotTV[category];
        } catch (error) {
            console.error(`获取${category}热门电视剧失败:`, error);
            return [];
        }
    },

    /**
     * 搜索电影
     * @param {string} keyword - 搜索关键词
     * @returns {Promise<Array>} - 搜索结果数组
     */
    async searchMovies(keyword) {
        if (!keyword || keyword.trim().length === 0) {
            return [];
        }

        try {
            // 从所有数据中搜索
            const allMovies = [
                ...await this.getNowPlayingMovies(),
                ...await this.getHotMovies('hot'),
                ...await this.getHotMovies('latest'),
                ...await this.getHotMovies('highRated'),
                ...await this.getHotMovies('hiddenGems')
            ];

            const searchTerm = keyword.toLowerCase().trim();

            return allMovies.filter(movie => {
                return movie.title.toLowerCase().includes(searchTerm) ||
                       movie.originalTitle.toLowerCase().includes(searchTerm) ||
                       movie.directors.some(d => d.toLowerCase().includes(searchTerm)) ||
                       movie.casts.some(c => c.toLowerCase().includes(searchTerm)) ||
                       movie.genres.some(g => g.toLowerCase().includes(searchTerm));
            });
        } catch (error) {
            console.error('搜索电影失败:', error);
            return [];
        }
    },

    /**
     * 根据ID获取电影详情
     * @param {number} id - 电影ID
     * @returns {Promise<Object|null>} - 电影详情对象
     */
    async getMovieById(id) {
        try {
            // 从所有数据中查找
            const allMovies = [
                ...await this.getNowPlayingMovies(),
                ...await this.getHotMovies('hot'),
                ...await this.getHotMovies('latest'),
                ...await this.getHotMovies('highRated'),
                ...await this.getHotMovies('hiddenGems')
            ];

            return allMovies.find(movie => movie.id === id) || null;
        } catch (error) {
            console.error(`获取电影详情失败 (ID: ${id}):`, error);
            return null;
        }
    },

    /**
     * 清除缓存
     * @param {string} type - 缓存类型，如果未指定则清除所有缓存
     */
    clearCache(type) {
        if (type) {
            if (this.cache[type]) {
                if (Array.isArray(this.cache[type])) {
                    this.cache[type] = [];
                } else {
                    this.cache[type] = {};
                }
            }
        } else {
            // 清除所有缓存
            this.cache = {
                nowPlaying: [],
                hotMovies: {},
                weeklyChart: [],
                hotLists: [],
                hotReviews: [],
                hotTV: {}
            };
        }
    },

    /**
     * 获取加载状态
     * @param {string} type - 数据类型
     * @returns {boolean} - 是否正在加载
     */
    isLoading(type) {
        return this.loadingStates[type] || false;
    },

    /**
     * 获取错误信息
     * @param {string} type - 数据类型
     * @returns {string|null} - 错误信息
     */
    getError(type) {
        return this.errors[type] || null;
    },

    /**
     * 格式化电影数据
     * @param {Object} movie - 原始电影数据
     * @returns {Object} - 格式化后的电影数据
     */
    formatMovieData(movie) {
        // 确定最佳图片路径
        let bestImagePath = '';

        // 1. 优先使用本地图片
        if (movie.localPoster && movie.localPoster.trim()) {
            bestImagePath = movie.localPoster;
        }
        // 2. 其次使用原始URL
        else if (movie.poster && movie.poster.trim()) {
            bestImagePath = movie.poster;
        }
        // 3. 最后使用占位图（在渲染时生成）

        return {
            ...movie,
            ratingText: movie.rating > 0 ? movie.rating.toFixed(1) : '暂无评分',
            ratingClass: movie.rating >= 8 ? 'high' : movie.rating >= 7 ? 'medium' : 'low',
            yearText: movie.year.toString(),
            genresText: movie.genres.join(' / '),
            countriesText: movie.countries.join(' / '),
            directorsText: movie.directors.join(' / '),
            castsText: movie.casts.slice(0, 3).join(' / '),
            hasRating: movie.rating > 0,
            isNew: new Date(movie.releaseDate) > new Date(Date.now() - 30 * 24 * 60 * 60 * 1000),
            // 图片路径相关
            bestImagePath: bestImagePath,
            hasLocalPoster: !!(movie.localPoster && movie.localPoster.trim()),
            hasOriginalPoster: !!(movie.poster && movie.poster.trim())
        };
    }
};

// 初始化数据管理器
window.DataManager = DataManager.init();
