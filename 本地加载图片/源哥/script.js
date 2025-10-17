function loadImages() {
    const urlInput = document.getElementById('urlInput').value;
    const urls = urlInput.split(',');
    const imageContainer = document.getElementById('imageContainer');
    imageContainer.innerHTML = ''; // 清空之前的图片
    urls.forEach(url => {
        const img = document.createElement('img');
        img.src = url.trim();
        imageContainer.appendChild(img);
    });
}
function loadFromExcel() {
    const fileInput = document.getElementById('fileInput');
    const imageContainer = document.getElementById('imageContainer');
    imageContainer.innerHTML = ''; // 清空之前的图片
    if (fileInput.files.length === 0) {
        alert('请上传Excel文件');
        return;
    }
    const file = fileInput.files[0];
    const reader = new FileReader();
    reader.onload = function(event) {
        const data = event.target.result;
        const workbook = XLSX.read(data, {type: 'binary'});
        // 假设URL存储在第一个工作表的第一列
        const firstSheetName = workbook.SheetNames[0];
        const worksheet = workbook.Sheets[firstSheetName];
        const urls = XLSX.utils.sheet_to_json(worksheet, {header: 1}).map(row => row[0]);
        urls.forEach(url => {
            const img = document.createElement('img');
            img.src = url;
            imageContainer.appendChild(img);
        });
    };
    reader.readAsBinaryString(file);
}