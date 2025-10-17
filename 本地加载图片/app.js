// 全局变量
let urlList = [];
let imageStats = {
    total: 0,
    success: 0,
    error: 0
};

// 初始化
document.addEventListener('DOMContentLoaded', function() {
    // 绑定Excel文件上传事件
    document.getElementById('excelFile').addEventListener('change', handleExcelUpload);

    // 绑定URL输入框回车事件
    document.getElementById('urlInput').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            addUrl();
        }
    });

    // 从本地存储恢复数据
    loadFromLocalStorage();
});

// 切换标签页
function switchTab(tabName) {
    // 更新按钮状态
    document.querySelectorAll('.tab-button').forEach(btn => {
        btn.classList.remove('active');
    });
    document.querySelector(`.tab-button[onclick="switchTab('${tabName}')"]`).classList.add('active');

    // 更新内容显示
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });
    document.getElementById(`${tabName}-tab`).classList.add('active');
}

// 添加URL
function addUrl() {
    const urlInput = document.getElementById('urlInput');
    const url = urlInput.value.trim();

    if (!url) {
        alert('请输入有效的URL链接');
        return;
    }

    // 验证URL格式
    if (!isValidUrl(url)) {
        alert('请输入有效的URL格式（如：https://example.com/image.jpg）');
        return;
    }

    // 检查是否已存在
    if (urlList.includes(url)) {
        alert('该URL已存在');
        return;
    }

    urlList.push(url);
    urlInput.value = '';
    updateUrlListDisplay();
    saveToLocalStorage();
}

// 批量添加URL
function addBatchUrls() {
    const batchInput = document.getElementById('batchUrlInput');
    const inputText = batchInput.value.trim();

    if (!inputText) {
        alert('请输入URL链接');
        return;
    }

    // 解析URL：支持换行和逗号分隔
    const urls = parseBatchUrls(inputText);

    if (urls.length === 0) {
        alert('未找到有效的URL链接');
        return;
    }

    let addedCount = 0;
    let duplicateCount = 0;
    let invalidCount = 0;

    urls.forEach(url => {
        if (!isValidUrl(url)) {
            invalidCount++;
            return;
        }

        if (urlList.includes(url)) {
            duplicateCount++;
            return;
        }

        urlList.push(url);
        addedCount++;
    });

    updateUrlListDisplay();
    saveToLocalStorage();

    // 清空输入框
    batchInput.value = '';

    // 显示添加结果
    let message = `批量添加完成！\n`;
    if (addedCount > 0) message += `成功添加: ${addedCount} 个URL\n`;
    if (duplicateCount > 0) message += `重复跳过: ${duplicateCount} 个URL\n`;
    if (invalidCount > 0) message += `无效URL: ${invalidCount} 个`;

    alert(message);
}

// 验证URL格式
function isValidUrl(string) {
    try {
        new URL(string);
        return true;
    } catch (_) {
        return false;
    }
}

// 更新URL列表显示
function updateUrlListDisplay() {
    const urlListElement = document.getElementById('urlList');

    if (urlList.length === 0) {
        urlListElement.innerHTML = `
            <div style="text-align: center; color: #7f8c8d; padding: 20px;">
                暂无URL链接，请添加URL或上传Excel文件
            </div>
        `;
        return;
    }

    urlListElement.innerHTML = urlList.map((url, index) => `
        <div class="url-item">
            <span class="url-text">${url}</span>
            <button class="remove-url" onclick="removeUrl(${index})">删除</button>
        </div>
    `).join('');
}

// 删除URL
function removeUrl(index) {
    urlList.splice(index, 1);
    updateUrlListDisplay();
    saveToLocalStorage();
}

// 处理Excel文件上传
function handleExcelUpload(event) {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = function(e) {
        try {
            const data = new Uint8Array(e.target.result);
            const workbook = XLSX.read(data, { type: 'array' });

            // 获取第一个工作表
            const firstSheet = workbook.Sheets[workbook.SheetNames[0]];
            const jsonData = XLSX.utils.sheet_to_json(firstSheet);

            // 提取URL
            const extractedUrls = extractUrlsFromExcel(jsonData);

            if (extractedUrls.length === 0) {
                alert('未在Excel文件中找到有效的URL链接');
                return;
            }

            // 添加到URL列表
            extractedUrls.forEach(url => {
                if (isValidUrl(url) && !urlList.includes(url)) {
                    urlList.push(url);
                }
            });

            updateUrlListDisplay();
            saveToLocalStorage();

            alert(`成功从Excel文件中提取 ${extractedUrls.length} 个URL链接`);

        } catch (error) {
            console.error('Excel解析错误:', error);
            alert('Excel文件解析失败，请检查文件格式');
        }
    };

    reader.readAsArrayBuffer(file);
}

// 从Excel数据中提取URL
function extractUrlsFromExcel(data) {
    const urls = [];

    data.forEach(row => {
        // 遍历行的每个属性值
        Object.values(row).forEach(value => {
            if (typeof value === 'string' && isValidUrl(value)) {
                urls.push(value);
            }
        });
    });

    return urls;
}

// 加载所有图片
async function loadAllImages() {
    if (urlList.length === 0) {
        alert('请先添加URL链接或上传Excel文件');
        return;
    }

    // 显示加载动画
    showLoading(true);

    // 重置统计
    imageStats = { total: urlList.length, success: 0, error: 0 };
    updateStats();

    // 清空图片网格
    const imagesGrid = document.getElementById('imagesGrid');
    imagesGrid.innerHTML = '';

    // 批量加载图片
    const loadPromises = urlList.map(async (url, index) => {
        return await loadSingleImage(url, index);
    });

    // 等待所有图片加载完成
    await Promise.allSettled(loadPromises);

    // 隐藏加载动画
    showLoading(false);

    // 显示加载结果
    alert(`图片加载完成！\n成功: ${imageStats.success} 张\n失败: ${imageStats.error} 张`);
}

// 加载单张图片
async function loadSingleImage(url, index) {
    return new Promise((resolve) => {
        const imagesGrid = document.getElementById('imagesGrid');

        // 创建图片卡片
        const imageCard = document.createElement('div');
        imageCard.className = 'image-card';
        imageCard.innerHTML = `
            <div class="image-container">
                <div style="display: flex; justify-content: center; align-items: center; height: 100%; color: #7f8c8d;">
                    加载中...
                </div>
            </div>
            <div class="image-info">
                <div class="image-url">${url}</div>
                <span class="image-status status-loading">加载中</span>
            </div>
        `;

        imagesGrid.appendChild(imageCard);

        const img = new Image();

        img.onload = function() {
            imageStats.success++;
            updateStats();

            imageCard.innerHTML = `
                <div class="image-container">
                    <img src="${url}" alt="加载的图片" class="loaded-image" onclick="openImageInNewTab('${url}')" style="cursor: pointer;">
                </div>
                <div class="image-info">
                    <div class="image-url">${url}</div>
                    <span class="image-status status-success">加载成功</span>
                </div>
            `;
            resolve();
        };

        img.onerror = function() {
            imageStats.error++;
            updateStats();

            imageCard.innerHTML = `
                <div class="image-container">
                    <div style="display: flex; justify-content: center; align-items: center; height: 100%; background: #f8f9fa; color: #e74c3c;">
                        ❌ 图片加载失败
                    </div>
                </div>
                <div class="image-info">
                    <div class="image-url">${url}</div>
                    <span class="image-status status-error">加载失败</span>
                </div>
            `;
            resolve();
        };

        // 设置超时
        setTimeout(() => {
            if (!img.complete) {
                img.onerror();
            }
        }, 10000);

        img.src = url;
    });
}

// 在新标签页打开图片
function openImageInNewTab(url) {
    window.open(url, '_blank');
}

// 更新统计信息
function updateStats() {
    document.getElementById('totalCount').textContent = imageStats.total;
    document.getElementById('successCount').textContent = imageStats.success;
    document.getElementById('errorCount').textContent = imageStats.error;
}

// 显示/隐藏加载动画
function showLoading(show) {
    const loadingOverlay = document.getElementById('loadingOverlay');
    loadingOverlay.style.display = show ? 'flex' : 'none';
}

// 清空所有
function clearAll() {
    if (!confirm('确定要清空所有URL链接和图片吗？')) {
        return;
    }

    urlList = [];
    imageStats = { total: 0, success: 0, error: 0 };

    updateUrlListDisplay();
    updateStats();

    const imagesGrid = document.getElementById('imagesGrid');
    imagesGrid.innerHTML = `
        <div style="text-align: center; color: #7f8c8d; padding: 40px;">
            暂无图片，请添加URL链接或上传Excel文件后点击"加载所有图片"
        </div>
    `;

    // 清空文件输入
    document.getElementById('excelFile').value = '';

    saveToLocalStorage();
}

// 保存到本地存储
function saveToLocalStorage() {
    localStorage.setItem('imageLoader_urlList', JSON.stringify(urlList));
}

// 从本地存储加载
function loadFromLocalStorage() {
    const savedUrlList = localStorage.getItem('imageLoader_urlList');
    if (savedUrlList) {
        urlList = JSON.parse(savedUrlList);
        updateUrlListDisplay();
    }
}

// 解析批量URL输入
function parseBatchUrls(inputText) {
    // 先按换行分割
    let urls = inputText.split(/\r?\n/);

    // 如果只有一行，尝试按逗号分割
    if (urls.length === 1 && urls[0].includes(',')) {
        urls = urls[0].split(',');
    }

    // 清理每个URL
    return urls
        .map(url => url.trim())
        .filter(url => url.length > 0)
        .map(url => {
            // 移除可能的引号
            return url.replace(/^["']|["']$/g, '');
        });
}
