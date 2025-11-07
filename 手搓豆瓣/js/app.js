/**
 * 主应用逻辑
 * 实现页面交互和数据渲染
 */

// 应用主对象
const App = {
    // 当前状态
    state: {
        currentHotMovieCategory: 'hot',
        currentTVCategory: 'all',
        searchKeyword: '',
        isLoading: false,
        nowPlayingPage: 1,
        nowPlayingPerPage: 5,
        nowPlayingTotalPages: 1,
        hotMoviesPage: 1,
        hotMoviesPerPage: 10, // 确保每页10条数据
        hotMoviesTotalPages: 1
    },

    // DOM元素缓存
    elements: {},

    /**
     * 初始化应用
     */
    async init() {
        console.log('应用初始化');

        // 缓存DOM元素
        this.cacheElements();

        // 绑定事件
        this.bindEvents();

        // 加载初始数据
        await this.loadInitialData();

        // 初始化滚动到顶部按钮
        this.initScrollToTop();

        // 初始化图片预加载
        this.initImagePreloading();

        console.log('应用初始化完成');
    },

    /**
     * 缓存DOM元素
     */
    cacheElements() {
        this.elements = {
            // 搜索相关
            searchInput: document.getElementById('searchInput'),
            searchBtn: document.getElementById('searchBtn'),

            // 内容容器
            nowPlayingMovies: document.getElementById('nowPlayingMovies'),
            nowPlayingPagination: document.getElementById('nowPlayingPagination'),
            hotMoviesGrid: document.getElementById('hotMoviesGrid'),
            hotMoviesPagination: document.getElementById('hotMoviesPagination'),
            hotTVGrid: document.getElementById('hotTVGrid'),
            weeklyChart: document.getElementById('weeklyChart'),
            hotLists: document.getElementById('hotLists'),
            hotReviews: document.getElementById('hotReviews'),

            // 分类按钮
            hotMovieTabs: document.querySelectorAll('.hot-movies-section .tab-btn'),
            tvTabs: document.querySelectorAll('.hot-tv-section .tab-btn'),

            // 滚动到顶部按钮
            scrollToTopBtn: null
        };
    },

    /**
     * 绑定事件
     */
    bindEvents() {
        // 搜索事件
        if (this.elements.searchInput) {
            this.elements.searchInput.addEventListener('input',
                Utils.debounce((e) => this.handleSearch(e.target.value), 300)
            );
        }

        if (this.elements.searchBtn) {
            this.elements.searchBtn.addEventListener('click', () => {
                const keyword = this.elements.searchInput.value;
                this.handleSearch(keyword);
            });
        }

        // 热门电影分类切换
        this.elements.hotMovieTabs.forEach(tab => {
            tab.addEventListener('click', (e) => {
                const category = e.target.dataset.category;
                this.switchHotMovieCategory(category);
            });
        });

        // 电视剧分类切换
        this.elements.tvTabs.forEach(tab => {
            tab.addEventListener('click', (e) => {
                const category = e.target.dataset.category;
                this.switchTVCategory(category);
            });
        });

        // 回车搜索
        document.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && document.activeElement === this.elements.searchInput) {
                const keyword = this.elements.searchInput.value;
                this.handleSearch(keyword);
            }
        });
    },

    /**
     * 加载初始数据
     */
    async loadInitialData() {
        try {
            // 显示加载状态
            this.setLoading(true);

            // 并行加载所有数据
            const [
                nowPlayingMovies,
                hotMovies,
                weeklyChart,
                hotLists,
                hotReviews,
                hotTV
            ] = await Promise.all([
                DataManager.getNowPlayingMovies(),
                DataManager.getHotMovies('hot'),
                DataManager.getWeeklyChart(),
                DataManager.getHotLists(),
                DataManager.getHotReviews(),
                DataManager.getHotTV('all')
            ]);

            // 渲染数据
            this.renderNowPlayingMovies(nowPlayingMovies);
            this.renderHotMovies(hotMovies);
            this.renderWeeklyChart(weeklyChart);
            this.renderHotLists(hotLists);
            this.renderHotReviews(hotReviews);
            this.renderHotTV(hotTV);

        } catch (error) {
            console.error('加载初始数据失败:', error);
            // 显示更具体的错误信息
            Utils.showNotification(`加载数据失败: ${error.message}`, 'error');
        } finally {
            this.setLoading(false);
        }
    },

    /**
     * 渲染正在热映电影
     * @param {Array} movies - 电影数组
     */
    renderNowPlayingMovies(movies) {
        if (!this.elements.nowPlayingMovies) return;

        if (!movies || movies.length === 0) {
            Utils.showEmptyState(this.elements.nowPlayingMovies, '暂无热映电影', '当前没有正在热映的电影');
            return;
        }

        // 更新电影数量显示
        this.updateNowPlayingCount(movies.length);

        // 计算分页
        const totalMovies = movies.length;
        const totalPages = Math.ceil(totalMovies / this.state.nowPlayingPerPage);
        this.state.nowPlayingTotalPages = totalPages;

        // 获取当前页的电影
        const startIndex = (this.state.nowPlayingPage - 1) * this.state.nowPlayingPerPage;
        const endIndex = startIndex + this.state.nowPlayingPerPage;
        const currentPageMovies = movies.slice(startIndex, endIndex);

        // 渲染当前页的电影
        const html = currentPageMovies.map(movie => {
            const formattedMovie = DataManager.formatMovieData(movie);
            const imageSrc = formattedMovie.bestImagePath;
            const doubanMovieId = this.extractMovieId(formattedMovie.buyTicketUrl);
            const detailUrl = doubanMovieId ? `https://movie.douban.com/subject/${doubanMovieId}/?from=showing` : '#';

            return `
                <div class="movie-card-scroll" data-movie-id="${formattedMovie.id}" data-detail-url="${detailUrl}">
                    <div class="poster">
                        <img src="${imageSrc}" alt="${formattedMovie.title}" loading="lazy"
                             onerror="Utils.handleImageError(this, '', '${formattedMovie.title}')"
                             onload="this.classList.add('loaded')">
                    </div>
                    <div class="title" title="${formattedMovie.title}">${formattedMovie.title}</div>
                    <div class="rating ${formattedMovie.hasRating ? '' : 'no-rating'}">
                        ${formattedMovie.ratingText}
                    </div>
                    ${formattedMovie.buyTicketUrl ?
                        `<button class="buy-ticket" onclick="window.open('${formattedMovie.buyTicketUrl}', '_blank')">选座购票</button>` :
                        ''
                    }
                    <div class="movie-tooltip">
                        <div class="tooltip-content">
                            <h4>${formattedMovie.title}</h4>
                            <p><strong>上映时间：</strong>${formattedMovie.releaseDate}</p>
                            <p><strong>类型：</strong>${formattedMovie.genresText}</p>
                            <p><strong>制片国家：</strong>${formattedMovie.countriesText}</p>
                            <p><strong>导演：</strong>${formattedMovie.directorsText}</p>
                            <p><strong>主演：</strong>${formattedMovie.castsText}</p>
                            ${formattedMovie.duration ? `<p><strong>片长：</strong>${formattedMovie.duration}</p>` : ''}
                        </div>
                    </div>
                </div>
            `;
        }).join('');

        const paginationHtml = this.generatePaginationHtml();

        this.elements.nowPlayingMovies.innerHTML = html;
        this.elements.nowPlayingPagination.innerHTML = paginationHtml;

        // 绑定悬浮和点击事件
        this.bindMovieCardEvents();
        this.bindPaginationEvents();
    },

    /**
     * 更新正在热映电影数量显示
     * @param {number} totalCount - 总数量
     */
    updateNowPlayingCount(totalCount) {
        const countElement = document.getElementById('nowPlayingCount');
        if (countElement) {
            const currentPage = this.state.nowPlayingPage;
            const perPage = this.state.nowPlayingPerPage;
            const start = (currentPage - 1) * perPage + 1;
            const end = Math.min(currentPage * perPage, totalCount);

            countElement.textContent = `${start}-${end} / ${totalCount} 部`;
            countElement.title = `共 ${totalCount} 部电影，当前显示第 ${start}-${end} 部`;
        }
    },

    /**
     * 生成分页控件HTML
     */
    generatePaginationHtml() {
        const currentPage = this.state.nowPlayingPage;
        const totalPages = this.state.nowPlayingTotalPages;

        if (totalPages <= 1) {
            return '';
        }

        let html = '<div class="now-playing-pagination">';
        html += '<div class="page-info">';
        html += `第 ${currentPage} 页 / 共 ${totalPages} 页`;
        html += '</div>';
        html += '<div class="page-buttons">';

        // 上一页按钮
        if (currentPage > 1) {
            html += `<button class="page-btn prev-btn" data-page="${currentPage - 1}">上一页</button>`;
        } else {
            html += '<button class="page-btn prev-btn disabled" disabled>上一页</button>';
        }

        // 页码按钮（显示当前页附近的页码）
        const startPage = Math.max(1, currentPage - 1);
        const endPage = Math.min(totalPages, currentPage + 1);

        for (let i = startPage; i <= endPage; i++) {
            const activeClass = i === currentPage ? 'active' : '';
            html += `<button class="page-btn ${activeClass}" data-page="${i}">${i}</button>`;
        }

        // 如果页码范围较小，显示更多页码
        if (totalPages <= 5) {
            let fullHtml = '';
            for (let i = 1; i <= totalPages; i++) {
                const activeClass = i === currentPage ? 'active' : '';
                fullHtml += `<button class="page-btn ${activeClass}" data-page="${i}">${i}</button>`;
            }
            html = html.replace(/<button class="page-btn[^>]*data-page="[123]"[^>]*>[123]<\/button>/g, '');
            html += fullHtml;
        }

        // 下一页按钮
        if (currentPage < totalPages) {
            html += `<button class="page-btn next-btn" data-page="${currentPage + 1}">下一页</button>`;
        } else {
            html += '<button class="page-btn next-btn disabled" disabled>下一页</button>';
        }

        html += '</div>';
        html += '</div>';

        return html;
    },

    /**
     * 绑定分页事件
     */
    bindPaginationEvents() {
        const paginationButtons = document.querySelectorAll('.page-btn');
        paginationButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                if (button.classList.contains('disabled')) return;

                const page = parseInt(button.dataset.page);
                if (page && page !== this.state.nowPlayingPage) {
                    this.changeNowPlayingPage(page);
                }
            });
        });
    },

    /**
     * 切换正在热映页面
     * @param {number} page - 页码
     */
    async changeNowPlayingPage(page) {
        if (page < 1 || page > this.state.nowPlayingTotalPages) return;

        this.state.nowPlayingPage = page;

        // 重新渲染当前页
        const nowPlayingMovies = await DataManager.getNowPlayingMovies();
        this.renderNowPlayingMovies(nowPlayingMovies);

        // 滚动到正在热映区域
        this.scrollToNowPlaying();
    },

    /**
     * 滚动到正在热映区域
     */
    scrollToNowPlaying() {
        const nowPlayingSection = document.querySelector('.now-playing-section');
        if (nowPlayingSection) {
            nowPlayingSection.scrollIntoView({
                behavior: 'smooth',
                block: 'start',
                inline: 'nearest'
            });
        }
    },

    /**
     * 渲染热门电影
     * @param {Array} movies - 电影数组
     */
    renderHotMovies(movies) {
        if (!this.elements.hotMoviesGrid) return;

        if (!movies || movies.length === 0) {
            Utils.showEmptyState(this.elements.hotMoviesGrid, '暂无热门电影', '当前没有热门电影');
            return;
        }

        // 计算分页
        const totalMovies = movies.length;
        const totalPages = Math.ceil(totalMovies / this.state.hotMoviesPerPage);
        this.state.hotMoviesTotalPages = totalPages;

        // 获取当前页的电影
        const startIndex = (this.state.hotMoviesPage - 1) * this.state.hotMoviesPerPage;
        const endIndex = startIndex + this.state.hotMoviesPerPage;
        const currentPageMovies = movies.slice(startIndex, endIndex);

        const html = currentPageMovies.map(movie => {
            const formattedMovie = DataManager.formatMovieData(movie);
            // 使用最佳图片路径（优先本地图片）
            const imageSrc = formattedMovie.bestImagePath;
            // 提取豆瓣电影ID
            const doubanMovieId = this.extractMovieId(formattedMovie.buyTicketUrl);
            // 构建详情页URL
            const detailUrl = doubanMovieId ? `https://movie.douban.com/subject/${doubanMovieId}/?from=showing` : '#';

            return `
                <div class="movie-card" data-movie-id="${formattedMovie.id}" data-detail-url="${detailUrl}">
                    <div class="poster">
                        <img src="${imageSrc}" alt="${formattedMovie.title}" loading="lazy"
                             onerror="Utils.handleImageError(this, '', '${formattedMovie.title}')"
                             onload="this.classList.add('loaded')">
                    </div>
                    <div class="title" title="${formattedMovie.title}">${formattedMovie.title}</div>
                    <div class="rating ${formattedMovie.hasRating ? '' : 'no-rating'}">
                        ${formattedMovie.ratingText}
                    </div>
                    <div class="movie-tooltip">
                        <div class="tooltip-content">
                            <h4>${formattedMovie.title}</h4>
                            <p><strong>上映时间：</strong>${formattedMovie.releaseDate}</p>
                            <p><strong>类型：</strong>${formattedMovie.genresText}</p>
                            <p><strong>制片国家：</strong>${formattedMovie.countriesText}</p>
                            <p><strong>导演：</strong>${formattedMovie.directorsText}</p>
                            <p><strong>主演：</strong>${formattedMovie.castsText}</p>
                            ${formattedMovie.duration ? `<p><strong>片长：</strong>${formattedMovie.duration}</p>` : ''}
                        </div>
                    </div>
                </div>
            `;
        }).join('');

        this.elements.hotMoviesGrid.innerHTML = html;

        // 渲染分页
        const paginationHtml = this.generateHotMoviesPaginationHtml();
        this.elements.hotMoviesPagination.innerHTML = paginationHtml;

        // 绑定事件
        this.bindMovieCardEvents();
        this.bindHotMoviesPaginationEvents();
    },

    /**
     * 渲染一周口碑榜
     * @param {Array} chart - 口碑榜数组
     */
    renderWeeklyChart(chart) {
        if (!this.elements.weeklyChart) return;

        if (!chart || chart.length === 0) {
            Utils.showEmptyState(this.elements.weeklyChart, '暂无口碑榜', '当前没有口碑榜数据');
            return;
        }

        const html = chart.map(item => `
            <div class="weekly-chart-item">
                <div class="chart-rank ${item.rank <= 3 ? 'top3' : ''}">${item.rank}</div>
                <div class="chart-info">
                    <div class="chart-title">${item.title}</div>
                    <div class="chart-rating">${Utils.formatRating(item.rating)}</div>
                </div>
            </div>
        `).join('');

        this.elements.weeklyChart.innerHTML = html;
    },

    /**
     * 渲染热门片单
     * @param {Array} lists - 片单数组
     */
    renderHotLists(lists) {
        if (!this.elements.hotLists) return;

        if (!lists || lists.length === 0) {
            Utils.showEmptyState(this.elements.hotLists, '暂无热门片单', '当前没有热门片单');
            return;
        }

        const html = lists.map(list => `
            <div class="hot-list-item">
                <div class="hot-list-title">${list.title}</div>
                <div class="hot-list-meta">${list.movieCount}部 / ${list.followerCount}人关注</div>
            </div>
        `).join('');

        this.elements.hotLists.innerHTML = html;
    },

    /**
     * 渲染热门影评
     * @param {Array} reviews - 影评数组
     */
    renderHotReviews(reviews) {
        if (!this.elements.hotReviews) return;

        if (!reviews || reviews.length === 0) {
            Utils.showEmptyState(this.elements.hotReviews, '暂无热门影评', '当前没有热门影评');
            return;
        }

        const html = reviews.map(review => `
            <div class="hot-review-item">
                <div class="review-movie-title">《${review.movieTitle}》</div>
                <div class="review-title">${review.reviewTitle}</div>
                <div class="review-author">${review.author} 评论</div>
            </div>
        `).join('');

        this.elements.hotReviews.innerHTML = html;
    },

    /**
     * 渲染热门电视剧
     * @param {Array} tvShows - 电视剧数组
     */
    renderHotTV(tvShows) {
        if (!this.elements.hotTVGrid) return;

        if (!tvShows || tvShows.length === 0) {
            Utils.showEmptyState(this.elements.hotTVGrid, '暂无热门电视剧', '当前没有热门电视剧');
            return;
        }

        const html = tvShows.map(tv => {
            const ratingText = tv.rating > 0 ? tv.rating.toFixed(1) : '暂无评分';
            // 使用最佳图片路径（优先本地图片）
            const imageSrc = tv.localPoster || tv.poster;
            // 提取豆瓣电影ID（电视剧也使用相同的ID格式）
            const doubanMovieId = this.extractMovieId(tv.poster); // 从poster URL中提取ID
            // 构建详情页URL
            const detailUrl = doubanMovieId ? `https://movie.douban.com/subject/${doubanMovieId}/?from=showing` : '#';

            return `
                <div class="movie-card" data-tv-id="${tv.id}" data-detail-url="${detailUrl}">
                    <div class="poster">
                        <img src="${imageSrc}" alt="${tv.title}" loading="lazy"
                             onerror="Utils.handleImageError(this, '', '${tv.title}')"
                             onload="this.classList.add('loaded')">
                    </div>
                    <div class="title" title="${tv.title}">${tv.title}</div>
                    <div class="rating ${tv.rating > 0 ? '' : 'no-rating'}">
                        ${ratingText}
                    </div>
                    <div class="movie-tooltip">
                        <div class="tooltip-content">
                            <h4>${tv.title}</h4>
                            <p><strong>年份：</strong>${tv.year}</p>
                            <p><strong>类型：</strong>${tv.genres.join(' / ')}</p>
                            <p><strong>制片国家：</strong>${tv.countries.join(' / ')}</p>
                            <p><strong>集数：</strong>${tv.episodes}集</p>
                            <p><strong>状态：</strong>${tv.status}</p>
                        </div>
                    </div>
                </div>
            `;
        }).join('');

        this.elements.hotTVGrid.innerHTML = html;
    },

    /**
     * 切换热门电影分类
     * @param {string} category - 分类
     */
    async switchHotMovieCategory(category) {
        if (this.state.currentHotMovieCategory === category) return;

        // 更新状态并重置页码
        this.state.currentHotMovieCategory = category;
        this.state.hotMoviesPage = 1;

        // 更新UI
        this.elements.hotMovieTabs.forEach(tab => {
            tab.classList.toggle('active', tab.dataset.category === category);
        });

        // 显示加载状态
        Utils.showLoading(this.elements.hotMoviesGrid);

        try {
            // 获取新数据
            const movies = await DataManager.getHotMovies(category);
            this.renderHotMovies(movies);
        } catch (error) {
            console.error(`切换热门电影分类失败: ${category}`, error);
            Utils.showError(this.elements.hotMoviesGrid, '加载失败，请重试', () => {
                this.switchHotMovieCategory(category);
            });
        }
    },

    /**
     * 切换电视剧分类
     * @param {string} category - 分类
     */
    async switchTVCategory(category) {
        if (this.state.currentTVCategory === category) return;

        // 更新状态
        this.state.currentTVCategory = category;

        // 更新UI
        this.elements.tvTabs.forEach(tab => {
            tab.classList.toggle('active', tab.dataset.category === category);
        });

        // 显示加载状态
        Utils.showLoading(this.elements.hotTVGrid);

        try {
            // 获取新数据
            const tvShows = await DataManager.getHotTV(category);
            this.renderHotTV(tvShows);
        } catch (error) {
            console.error(`切换电视剧分类失败: ${category}`, error);
            Utils.showError(this.elements.hotTVGrid, '加载失败，请重试', () => {
                this.switchTVCategory(category);
            });
        }
    },

    /**
     * 处理搜索
     * @param {string} keyword - 搜索关键词
     */
    async handleSearch(keyword) {
        if (!keyword || keyword.trim().length === 0) {
            // 如果搜索关键词为空，重新加载当前数据
            await this.loadInitialData();
            return;
        }

        this.state.searchKeyword = keyword.trim();

        try {
            this.setLoading(true);

            // 搜索电影
            const searchResults = await DataManager.searchMovies(keyword);

            if (searchResults.length === 0) {
                // 显示无结果状态
                Utils.showEmptyState(
                    this.elements.hotMoviesGrid,
                    '未找到相关电影',
                    `没有找到包含 "${keyword}" 的电影`
                );
                return;
            }

            // 显示搜索结果
            this.renderHotMovies(searchResults);

            // 显示搜索成功通知
            Utils.showNotification(`找到 ${searchResults.length} 部相关电影`, 'success', 2000);

        } catch (error) {
            console.error('搜索失败:', error);
            Utils.showNotification('搜索失败，请重试', 'error');
        } finally {
            this.setLoading(false);
        }
    },

    /**
     * 绑定电影卡片事件
     */
    bindMovieCardEvents() {
        // 绑定电影卡片点击事件
        const movieCards = document.querySelectorAll('.movie-card, .movie-card-scroll');
        movieCards.forEach(card => {
            // 点击事件 - 跳转到详情页
            card.addEventListener('click', (e) => {
                // 如果点击的是购票按钮，不跳转
                if (e.target.classList.contains('buy-ticket')) {
                    return;
                }

                const detailUrl = card.dataset.detailUrl;
                if (detailUrl && detailUrl !== '#') {
                    window.open(detailUrl, '_blank');
                } else {
                    Utils.showNotification('暂无详情页面', 'info');
                }
            });

            // 鼠标进入事件 - 显示悬浮信息
            card.addEventListener('mouseenter', (e) => {
                const tooltip = card.querySelector('.movie-tooltip');
                if (tooltip) {
                    tooltip.style.display = 'block';
                }
                // 改变鼠标样式为可点击
                card.style.cursor = 'pointer';
            });

            // 鼠标离开事件 - 隐藏悬浮信息
            card.addEventListener('mouseleave', (e) => {
                const tooltip = card.querySelector('.movie-tooltip');
                if (tooltip) {
                    tooltip.style.display = 'none';
                }
                // 恢复鼠标样式
                card.style.cursor = 'default';
            });
        });
    },

    /**
     * 处理电影点击
     * @param {number} movieId - 电影ID
     */
    handleMovieClick(movieId) {
        // 这里可以实现跳转到电影详情页的逻辑
        console.log(`点击了电影: ${movieId}`);
        Utils.showNotification(`点击了电影 ID: ${movieId}`, 'info', 1500);

        // 实际项目中可以跳转到详情页
        // window.location.href = `/movie/${movieId}`;
    },

    /**
     * 处理电视剧点击
     * @param {number} tvId - 电视剧ID
     */
    handleTVClick(tvId) {
        // 这里可以实现跳转到电视剧详情页的逻辑
        console.log(`点击了电视剧: ${tvId}`);
        Utils.showNotification(`点击了电视剧 ID: ${tvId}`, 'info', 1500);

        // 实际项目中可以跳转到详情页
        // window.location.href = `/tv/${tvId}`;
    },

    /**
     * 设置加载状态
     * @param {boolean} isLoading - 是否加载中
     */
    setLoading(isLoading) {
        this.state.isLoading = isLoading;

        // 可以在这里添加全局加载状态的UI处理
        if (isLoading) {
            document.body.classList.add('loading');
        } else {
            document.body.classList.remove('loading');
        }
    },

    /**
     * 初始化滚动到顶部按钮
     */
    initScrollToTop() {
        // 创建滚动到顶部按钮
        const scrollBtn = document.createElement('button');
        scrollBtn.className = 'scroll-to-top';
        scrollBtn.innerHTML = '↑';
        scrollBtn.title = '回到顶部';
        document.body.appendChild(scrollBtn);

        this.elements.scrollToTopBtn = scrollBtn;

        // 监听滚动事件
        window.addEventListener('scroll', Utils.throttle(() => {
            if (window.pageYOffset > 300) {
                scrollBtn.classList.add('show');
            } else {
                scrollBtn.classList.remove('show');
            }
        }, 100));

        // 点击事件
        scrollBtn.addEventListener('click', () => {
            Utils.smoothScrollTo('body');
        });
    },

    /**
     * 初始化图片懒加载
     */
    initLazyLoad() {
        const images = document.querySelectorAll('img[loading="lazy"]');
        images.forEach(img => {
            if (img.dataset.src) {
                Utils.lazyLoadImage(img, img.dataset.src);
            }
        });
    },

    /**
     * 初始化图片预加载
     */
    initImagePreloading() {
        // 预加载可见区域的图片
        const images = document.querySelectorAll('img[loading="lazy"]');
        images.forEach(img => {
            if (Utils.isInViewport(img, 0.5)) {
                this.loadImageWithFallback(img);
            }
        });

        // 监听滚动，加载更多图片
        window.addEventListener('scroll',
            Utils.throttle(() => this.loadVisibleImages(), 200)
        );
    },

    /**
     * 加载可见区域的图片
     */
    loadVisibleImages() {
        const images = document.querySelectorAll('img[loading="lazy"]:not(.loaded)');
        images.forEach(img => {
            if (Utils.isInViewport(img, 0.3)) {
                this.loadImageWithFallback(img);
            }
        });
    },

    /**
     * 加载图片并处理错误
     * @param {Element} img - 图片元素
     */
    loadImageWithFallback(img) {
        if (img.dataset.loading) return; // 已经在加载中

        img.dataset.loading = 'true';

        // 创建新图片对象来预加载
        const tempImg = new Image();

        tempImg.onload = () => {
            img.src = tempImg.src;
            img.classList.add('loaded');
            img.classList.remove('error');
            delete img.dataset.loading;
        };

        tempImg.onerror = () => {
            // 如果本地图片加载失败，尝试原始URL
            if (img.dataset.originalSrc && img.src !== img.dataset.originalSrc) {
                img.src = img.dataset.originalSrc;
            } else {
                // 使用占位图
                Utils.handleImageError(img, img.alt || '图片');
            }
            delete img.dataset.loading;
        };

        // 开始加载
        tempImg.src = img.src;
    },

    /**
     * 提取豆瓣电影ID
     * @param {string} buyTicketUrl - 购票URL
     * @returns {string|null} - 豆瓣电影ID
     */
    extractMovieId(buyTicketUrl) {
        if (!buyTicketUrl) return null;

        try {
            // 从购票URL中提取movie_id参数
            const url = new URL(buyTicketUrl);
            const movieId = url.searchParams.get('movie_id');
            return movieId;
        } catch (error) {
            // 如果不是标准URL，尝试正则提取
            const match = buyTicketUrl.match(/movie_id=(\d+)/);
            return match ? match[1] : null;
        }
    },

    /**
     * 生成热门电影分页控件HTML
     */
    generateHotMoviesPaginationHtml() {
        const currentPage = this.state.hotMoviesPage;
        const totalPages = this.state.hotMoviesTotalPages;

        if (totalPages <= 1) {
            return '';
        }

        let html = '<div class="pagination-controls">';
        html += '<div class="pagination-info">';
        html += `第 ${currentPage} 页 / 共 ${totalPages} 页`;
        html += '</div>';
        html += '<div class="pagination-buttons">';

        // 上一页按钮
        if (currentPage > 1) {
            html += `<button class="pagination-btn prev-btn" data-page="${currentPage - 1}">上一页</button>`;
        } else {
            html += '<button class="pagination-btn prev-btn disabled" disabled>上一页</button>';
        }

        // 页码按钮
        const startPage = Math.max(1, currentPage - 2);
        const endPage = Math.min(totalPages, currentPage + 2);

        for (let i = startPage; i <= endPage; i++) {
            const activeClass = i === currentPage ? 'active' : '';
            html += `<button class="pagination-btn page-btn ${activeClass}" data-page="${i}">${i}</button>`;
        }

        // 下一页按钮
        if (currentPage < totalPages) {
            html += `<button class="pagination-btn next-btn" data-page="${currentPage + 1}">下一页</button>`;
        } else {
            html += '<button class="pagination-btn next-btn disabled" disabled>下一页</button>';
        }

        html += '</div>';
        html += '</div>';

        return html;
    },

    /**
     * 绑定热门电影分页事件
     */
    bindHotMoviesPaginationEvents() {
        const paginationButtons = document.querySelectorAll('#hotMoviesPagination .pagination-btn');
        paginationButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                if (button.classList.contains('disabled')) return;

                const page = parseInt(button.dataset.page);
                if (page && page !== this.state.hotMoviesPage) {
                    this.changeHotMoviesPage(page);
                }
            });
        });
    },

    /**
     * 切换热门电影页面
     * @param {number} page - 页码
     */
    async changeHotMoviesPage(page) {
        if (page < 1 || page > this.state.hotMoviesTotalPages) return;

        this.state.hotMoviesPage = page;

        // 重新渲染当前页
        const movies = await DataManager.getHotMovies(this.state.currentHotMovieCategory);
        this.renderHotMovies(movies);

        // 滚动到热门电影区域
        const hotMoviesSection = document.querySelector('.hot-movies-section');
        if (hotMoviesSection) {
            hotMoviesSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    }
};

// 页面加载完成后初始化应用
document.addEventListener('DOMContentLoaded', () => {
    App.init();
});

// 导出App对象供其他模块使用
window.App = App;
