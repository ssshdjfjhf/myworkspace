/**
 * 工具函数模块
 * 包含常用的工具函数
 */

// 工具函数对象
const Utils = {
    /**
     * 防抖函数
     * @param {Function} func - 要执行的函数
     * @param {number} wait - 等待时间（毫秒）
     * @returns {Function} - 防抖后的函数
     */
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    /**
     * 节流函数
     * @param {Function} func - 要执行的函数
     * @param {number} limit - 时间限制（毫秒）
     * @returns {Function} - 节流后的函数
     */
    throttle(func, limit) {
        let inThrottle;
        return function(...args) {
            if (!inThrottle) {
                func.apply(this, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    },

    /**
     * 格式化日期
     * @param {string|Date} date - 日期字符串或Date对象
     * @param {string} format - 格式字符串
     * @returns {string} - 格式化后的日期字符串
     */
    formatDate(date, format = 'YYYY-MM-DD') {
        const d = new Date(date);
        const year = d.getFullYear();
        const month = String(d.getMonth() + 1).padStart(2, '0');
        const day = String(d.getDate()).padStart(2, '0');
        const hours = String(d.getHours()).padStart(2, '0');
        const minutes = String(d.getMinutes()).padStart(2, '0');
        const seconds = String(d.getSeconds()).padStart(2, '0');

        return format
            .replace('YYYY', year)
            .replace('MM', month)
            .replace('DD', day)
            .replace('HH', hours)
            .replace('mm', minutes)
            .replace('ss', seconds);
    },

    /**
     * 格式化数字（添加千位分隔符）
     * @param {number} num - 要格式化的数字
     * @returns {string} - 格式化后的字符串
     */
    formatNumber(num) {
        if (num === null || num === undefined) return '0';
        return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    },

    /**
     * 格式化评分
     * @param {number} rating - 评分
     * @returns {string} - 格式化后的评分字符串
     */
    formatRating(rating) {
        if (!rating || rating === 0) return '暂无评分';
        return rating.toFixed(1);
    },

    /**
     * 生成星级评分HTML
     * @param {number} rating - 评分（0-10）
     * @returns {string} - 星级评分HTML
     */
    generateStars(rating) {
        if (!rating || rating === 0) return '';

        const fullStars = Math.floor(rating / 2);
        const halfStar = (rating % 2) >= 1 ? 1 : 0;
        const emptyStars = 5 - fullStars - halfStar;

        let starsHTML = '';

        // 满星
        for (let i = 0; i < fullStars; i++) {
            starsHTML += '<span class="star">★</span>';
        }

        // 半星
        if (halfStar) {
            starsHTML += '<span class="star half">★</span>';
        }

        // 空星
        for (let i = 0; i < emptyStars; i++) {
            starsHTML += '<span class="star empty">★</span>';
        }

        return starsHTML;
    },

    /**
     * 截断文本
     * @param {string} text - 原文本
     * @param {number} maxLength - 最大长度
     * @param {string} suffix - 后缀
     * @returns {string} - 截断后的文本
     */
    truncateText(text, maxLength = 100, suffix = '...') {
        if (!text || text.length <= maxLength) return text;
        return text.substring(0, maxLength) + suffix;
    },

    /**
     * 获取URL参数
     * @param {string} name - 参数名
     * @returns {string|null} - 参数值
     */
    getURLParam(name) {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get(name);
    },

    /**
     * 设置URL参数
     * @param {Object} params - 参数对象
     */
    setURLParams(params) {
        const url = new URL(window.location);
        Object.keys(params).forEach(key => {
            if (params[key] === null || params[key] === undefined) {
                url.searchParams.delete(key);
            } else {
                url.searchParams.set(key, params[key]);
            }
        });
        window.history.replaceState({}, '', url);
    },

    /**
     * 平滑滚动到指定元素
     * @param {string|Element} target - 目标元素或选择器
     * @param {number} offset - 偏移量
     */
    smoothScrollTo(target, offset = 0) {
        const element = typeof target === 'string' ? document.querySelector(target) : target;
        if (!element) return;

        const targetPosition = element.offsetTop + offset;
        const startPosition = window.pageYOffset;
        const distance = targetPosition - startPosition;
        const duration = 500;
        let start = null;

        function animation(currentTime) {
            if (start === null) start = currentTime;
            const timeElapsed = currentTime - start;
            const run = ease(timeElapsed, startPosition, distance, duration);
            window.scrollTo(0, run);
            if (timeElapsed < duration) requestAnimationFrame(animation);
        }

        function ease(t, b, c, d) {
            t /= d / 2;
            if (t < 1) return c / 2 * t * t + b;
            t--;
            return -c / 2 * (t * (t - 2) - 1) + b;
        }

        requestAnimationFrame(animation);
    },

    /**
     * 检查元素是否在视口中
     * @param {Element} element - 要检查的元素
     * @param {number} threshold - 阈值（0-1）
     * @returns {boolean} - 是否在视口中
     */
    isInViewport(element, threshold = 0.1) {
        const rect = element.getBoundingClientRect();
        const windowHeight = window.innerHeight || document.documentElement.clientHeight;
        const windowWidth = window.innerWidth || document.documentElement.clientWidth;

        return (
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= windowHeight + (rect.height * threshold) &&
            rect.right <= windowWidth + (rect.width * threshold)
        );
    },

    /**
     * 图片懒加载
     * @param {Element} img - 图片元素
     * @param {string} src - 图片地址
     */
    lazyLoadImage(img, src) {
        if (!img || !src) return;

        // 添加加载类
        img.classList.add('lazy-image');

        // 使用 Intersection Observer
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const image = entry.target;
                    image.src = src;
                    image.classList.remove('lazy-image');
                    observer.unobserve(image);
                }
            });
        }, {
            rootMargin: '50px 0px',
            threshold: 0.01
        });

        observer.observe(img);
    },

    /**
     * 显示加载动画
     * @param {Element} container - 容器元素
     */
    showLoading(container) {
        if (!container) return;

        const loadingHTML = `
            <div class="loading-container">
                <div class="loading"></div>
                <p>加载中...</p>
            </div>
        `;

        container.innerHTML = loadingHTML;
    },

    /**
     * 显示错误信息
     * @param {Element} container - 容器元素
     * @param {string} message - 错误信息
     * @param {Function} retryCallback - 重试回调函数
     */
    showError(container, message, retryCallback) {
        if (!container) return;

        const errorHTML = `
            <div class="error-message">
                <p>${message}</p>
                ${retryCallback ? '<button class="retry-btn" onclick="retryCallback()">重试</button>' : ''}
            </div>
        `;

        container.innerHTML = errorHTML;

        // 绑定重试事件
        if (retryCallback) {
            const retryBtn = container.querySelector('.retry-btn');
            if (retryBtn) {
                retryBtn.addEventListener('click', retryCallback);
            }
        }
    },

    /**
     * 显示空状态
     * @param {Element} container - 容器元素
     * @param {string} title - 标题
     * @param {string} description - 描述
     */
    showEmptyState(container, title = '暂无数据', description = '没有找到相关内容') {
        if (!container) return;

        const emptyHTML = `
            <div class="empty-state">
                <div class="empty-icon">📭</div>
                <div class="empty-title">${title}</div>
                <div class="empty-desc">${description}</div>
            </div>
        `;

        container.innerHTML = emptyHTML;
    },

    /**
     * 创建通知
     * @param {string} message - 通知内容
     * @param {string} type - 通知类型（success, error, warning, info）
     * @param {number} duration - 显示时长（毫秒）
     */
    showNotification(message, type = 'info', duration = 3000) {
        // 创建通知元素
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;

        const title = type === 'success' ? '成功' :
                     type === 'error' ? '错误' :
                     type === 'warning' ? '警告' : '提示';

        notification.innerHTML = `
            <div class="notification-header">
                <div class="notification-title">${title}</div>
                <button class="notification-close">&times;</button>
            </div>
            <div class="notification-body">${message}</div>
        `;

        document.body.appendChild(notification);

        // 自动移除
        const removeNotification = () => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        };

        // 绑定关闭事件
        const closeBtn = notification.querySelector('.notification-close');
        closeBtn.addEventListener('click', removeNotification);

        // 定时移除
        if (duration > 0) {
            setTimeout(removeNotification, duration);
        }
    },

    /**
     * 生成唯一ID
     * @returns {string} - 唯一ID
     */
    generateId() {
        return Date.now().toString(36) + Math.random().toString(36).substr(2);
    },

    /**
     * 深拷贝对象
     * @param {Object} obj - 要拷贝的对象
     * @returns {Object} - 拷贝后的对象
     */
    deepClone(obj) {
        if (obj === null || typeof obj !== 'object') return obj;
        if (obj instanceof Date) return new Date(obj.getTime());
        if (obj instanceof Array) return obj.map(item => this.deepClone(item));
        if (typeof obj === 'object') {
            const cloned = {};
            for (const key in obj) {
                if (obj.hasOwnProperty(key)) {
                    cloned[key] = this.deepClone(obj[key]);
                }
            }
            return cloned;
        }
    },

    /**
     * 存储数据到localStorage
     * @param {string} key - 键名
     * @param {any} value - 值
     * @param {number} expireTime - 过期时间（毫秒）
     */
    setStorage(key, value, expireTime) {
        try {
            const data = {
                value: value,
                expire: expireTime ? Date.now() + expireTime : null
            };
            localStorage.setItem(key, JSON.stringify(data));
        } catch (error) {
            console.error('存储数据失败:', error);
        }
    },

    /**
     * 从localStorage获取数据
     * @param {string} key - 键名
     * @returns {any} - 存储的值
     */
    getStorage(key) {
        try {
            const data = localStorage.getItem(key);
            if (!data) return null;

            const parsed = JSON.parse(data);

            // 检查是否过期
            if (parsed.expire && Date.now() > parsed.expire) {
                localStorage.removeItem(key);
                return null;
            }

            return parsed.value;
        } catch (error) {
            console.error('获取存储数据失败:', error);
            return null;
        }
    },

    /**
     * 删除localStorage中的数据
     * @param {string} key - 键名
     */
    removeStorage(key) {
        try {
            localStorage.removeItem(key);
        } catch (error) {
            console.error('删除存储数据失败:', error);
        }
    },

    /**
     * 清除所有localStorage数据
     */
    clearStorage() {
        try {
            localStorage.clear();
        } catch (error) {
            console.error('清除存储数据失败:', error);
        }
    },

    /**
     * 处理图片加载错误
     * @param {Element} img - 图片元素
     * @param {string} fallbackSrc - 备用图片地址
     */
    handleImageError(img, fallbackSrc = '') {
        // 移除事件监听器避免循环
        img.onerror = null;

        // 使用备用图片或生成占位图
        if (fallbackSrc) {
            img.src = fallbackSrc;
        } else {
            // 生成SVG占位图
            const width = img.width || 150;
            const height = img.height || 210;
            const title = img.alt || '电影海报';

            img.src = this.generatePlaceholderSVG(width, height, title);
        }

        // 添加错误样式
        img.style.opacity = '0.7';
        img.style.filter = 'grayscale(30%)';
    },

    /**
     * 生成SVG占位图
     * @param {number} width - 宽度
     * @param {number} height - 高度
     * @param {string} text - 文字
     * @returns {string} - SVG data URL
     */
    generatePlaceholderSVG(width, height, text) {
        const encodedText = encodeURIComponent(text);
        const color1 = '#f0f0f0';
        const color2 = '#e0e0e0';

        return `data:image/svg+xml;base64,${btoa(`
            <svg width="${width}" height="${height}" xmlns="http://www.w3.org/2000/svg">
                <defs>
                    <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" style="stop-color:${color1};stop-opacity:1" />
                        <stop offset="100%" style="stop-color:${color2};stop-opacity:1" />
                    </linearGradient>
                </defs>
                <rect width="100%" height="100%" fill="url(#grad)" />
                <text x="50%" y="50%" text-anchor="middle" dy=".3em"
                      font-family="Arial, sans-serif" font-size="14" fill="#999">
                    ${text}
                </text>
            </svg>
        `)}`;
    },

    /**
     * 为图片添加错误处理
     * @param {Element} img - 图片元素
     * @param {string} fallbackSrc - 备用图片地址
     */
    addImageErrorHandler(img, fallbackSrc = '') {
        img.addEventListener('error', () => {
            this.handleImageError(img, fallbackSrc);
        });
    }
};

// 将工具函数挂载到全局对象
window.Utils = Utils;
