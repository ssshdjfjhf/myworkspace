// 待办事项应用的主要功能
class TodoApp {
    constructor() {
        this.todos = this.loadTodos();
        this.currentFilter = 'all';
        this.init();
    }

    // 初始化应用
    init() {
        this.bindEvents();
        this.render();
        this.updateStats();
    }

    // 绑定事件监听器
    bindEvents() {
        const todoInput = document.getElementById('todoInput');
        const addBtn = document.getElementById('addBtn');
        const filterBtns = document.querySelectorAll('.filter-btn');

        // 添加待办事项
        addBtn.addEventListener('click', () => this.addTodo());
        todoInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.addTodo();
            }
        });

        // 过滤按钮
        filterBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.setFilter(e.target.dataset.filter);
            });
        });
    }

    // 添加新的待办事项
    addTodo() {
        const todoInput = document.getElementById('todoInput');
        const prioritySelect = document.getElementById('prioritySelect');
        const text = todoInput.value.trim();

        if (text === '') {
            this.showNotification('请输入待办事项内容', 'error');
            return;
        }

        const todo = {
            id: Date.now(),
            text: text,
            completed: false,
            priority: prioritySelect.value,
            createdAt: new Date().toISOString()
        };

        this.todos.unshift(todo);
        this.saveTodos();
        this.render();
        this.updateStats();

        // 清空输入框
        todoInput.value = '';
        prioritySelect.value = 'medium';

        this.showNotification('待办事项添加成功！', 'success');
    }

    // 切换待办事项完成状态
    toggleTodo(id) {
        const todo = this.todos.find(t => t.id === id);
        if (todo) {
            todo.completed = !todo.completed;
            this.saveTodos();
            this.render();
            this.updateStats();
        }
    }

    // 删除待办事项
    deleteTodo(id) {
        const todoElement = document.querySelector(`[data-id="${id}"]`);
        if (todoElement) {
            todoElement.classList.add('removing');
            setTimeout(() => {
                this.todos = this.todos.filter(t => t.id !== id);
                this.saveTodos();
                this.render();
                this.updateStats();
                this.showNotification('待办事项已删除', 'info');
            }, 300);
        }
    }

    // 设置过滤器
    setFilter(filter) {
        this.currentFilter = filter;

        // 更新按钮状态
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-filter="${filter}"]`).classList.add('active');

        this.render();
    }

    // 获取过滤后的待办事项
    getFilteredTodos() {
        switch (this.currentFilter) {
            case 'completed':
                return this.todos.filter(todo => todo.completed);
            case 'pending':
                return this.todos.filter(todo => !todo.completed);
            default:
                return this.todos;
        }
    }

    // 渲染待办事项列表
    render() {
        const todoList = document.getElementById('todoList');
        const emptyState = document.getElementById('emptyState');
        const filteredTodos = this.getFilteredTodos();

        if (filteredTodos.length === 0) {
            todoList.innerHTML = '';
            emptyState.classList.add('show');
            return;
        }

        emptyState.classList.remove('show');

        todoList.innerHTML = filteredTodos.map(todo => `
            <div class="todo-item ${todo.completed ? 'completed' : ''} ${todo.priority}-priority" data-id="${todo.id}">
                <input type="checkbox" class="todo-checkbox" ${todo.completed ? 'checked' : ''}
                       onchange="todoApp.toggleTodo(${todo.id})">
                <span class="todo-text">${this.escapeHtml(todo.text)}</span>
                <span class="priority-badge priority-${todo.priority}">
                    ${this.getPriorityText(todo.priority)}
                </span>
                <button class="delete-btn" onclick="todoApp.deleteTodo(${todo.id})" title="删除">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        `).join('');
    }

    // 更新统计信息
    updateStats() {
        const totalTasks = document.getElementById('totalTasks');
        const completedTasks = document.getElementById('completedTasks');

        const total = this.todos.length;
        const completed = this.todos.filter(todo => todo.completed).length;

        totalTasks.textContent = total;
        completedTasks.textContent = completed;
    }

    // 获取优先级文本
    getPriorityText(priority) {
        const priorityMap = {
            'high': '高',
            'medium': '中',
            'low': '低'
        };
        return priorityMap[priority] || '中';
    }

    // HTML转义
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // 显示通知
    showNotification(message, type = 'info') {
        // 创建通知元素
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <i class="fas fa-${this.getNotificationIcon(type)}"></i>
            <span>${message}</span>
        `;

        // 添加样式
        Object.assign(notification.style, {
            position: 'fixed',
            top: '20px',
            right: '20px',
            padding: '15px 20px',
            borderRadius: '10px',
            color: 'white',
            fontWeight: '500',
            zIndex: '1000',
            display: 'flex',
            alignItems: 'center',
            gap: '10px',
            minWidth: '250px',
            boxShadow: '0 5px 15px rgba(0,0,0,0.2)',
            transform: 'translateX(100%)',
            transition: 'transform 0.3s ease'
        });

        // 设置背景色
        const colors = {
            success: '#28a745',
            error: '#dc3545',
            info: '#17a2b8',
            warning: '#ffc107'
        };
        notification.style.background = colors[type] || colors.info;

        document.body.appendChild(notification);

        // 显示动画
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 100);

        // 自动隐藏
        setTimeout(() => {
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 3000);
    }

    // 获取通知图标
    getNotificationIcon(type) {
        const icons = {
            success: 'check-circle',
            error: 'exclamation-circle',
            info: 'info-circle',
            warning: 'exclamation-triangle'
        };
        return icons[type] || icons.info;
    }

    // 保存到本地存储
    saveTodos() {
        localStorage.setItem('todos', JSON.stringify(this.todos));
    }

    // 从本地存储加载
    loadTodos() {
        const saved = localStorage.getItem('todos');
        return saved ? JSON.parse(saved) : [];
    }

    // 清空所有已完成的待办事项
    clearCompleted() {
        const completedCount = this.todos.filter(todo => todo.completed).length;
        if (completedCount === 0) {
            this.showNotification('没有已完成的待办事项', 'info');
            return;
        }

        if (confirm(`确定要删除 ${completedCount} 个已完成的待办事项吗？`)) {
            this.todos = this.todos.filter(todo => !todo.completed);
            this.saveTodos();
            this.render();
            this.updateStats();
            this.showNotification(`已删除 ${completedCount} 个已完成的待办事项`, 'success');
        }
    }

    // 导出待办事项
    exportTodos() {
        const dataStr = JSON.stringify(this.todos, null, 2);
        const dataBlob = new Blob([dataStr], {type: 'application/json'});
        const url = URL.createObjectURL(dataBlob);

        const link = document.createElement('a');
        link.href = url;
        link.download = `todos-${new Date().toISOString().split('T')[0]}.json`;
        link.click();

        URL.revokeObjectURL(url);
        this.showNotification('待办事项已导出', 'success');
    }

    // 导入待办事项
    importTodos(event) {
        const file = event.target.files[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = (e) => {
            try {
                const importedTodos = JSON.parse(e.target.result);
                if (Array.isArray(importedTodos)) {
                    this.todos = [...this.todos, ...importedTodos];
                    this.saveTodos();
                    this.render();
                    this.updateStats();
                    this.showNotification(`成功导入 ${importedTodos.length} 个待办事项`, 'success');
                } else {
                    throw new Error('Invalid format');
                }
            } catch (error) {
                this.showNotification('导入失败，文件格式不正确', 'error');
            }
        };
        reader.readAsText(file);
    }
}

// 初始化应用
let todoApp;

document.addEventListener('DOMContentLoaded', () => {
    todoApp = new TodoApp();

    // 添加键盘快捷键
    document.addEventListener('keydown', (e) => {
        // Ctrl/Cmd + Enter 快速添加
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            todoApp.addTodo();
        }

        // Escape 清空输入框
        if (e.key === 'Escape') {
            document.getElementById('todoInput').value = '';
        }
    });
});

// 添加右键菜单功能
document.addEventListener('contextmenu', (e) => {
    if (e.target.closest('.todo-item')) {
        e.preventDefault();
        // 这里可以添加右键菜单功能
    }
});

// 添加拖拽排序功能（简化版）
let draggedElement = null;

document.addEventListener('dragstart', (e) => {
    if (e.target.classList.contains('todo-item')) {
        draggedElement = e.target;
        e.target.style.opacity = '0.5';
    }
});

document.addEventListener('dragend', (e) => {
    if (e.target.classList.contains('todo-item')) {
        e.target.style.opacity = '';
        draggedElement = null;
    }
});

document.addEventListener('dragover', (e) => {
    e.preventDefault();
});

document.addEventListener('drop', (e) => {
    e.preventDefault();
    if (draggedElement && e.target.classList.contains('todo-item')) {
        const todoList = document.getElementById('todoList');
        const afterElement = getDragAfterElement(todoList, e.clientY);

        if (afterElement == null) {
            todoList.appendChild(draggedElement);
        } else {
            todoList.insertBefore(draggedElement, afterElement);
        }
    }
});

function getDragAfterElement(container, y) {
    const draggableElements = [...container.querySelectorAll('.todo-item:not(.dragging)')];

    return draggableElements.reduce((closest, child) => {
        const box = child.getBoundingClientRect();
        const offset = y - box.top - box.height / 2;

        if (offset < 0 && offset > closest.offset) {
            return { offset: offset, element: child };
        } else {
            return closest;
        }
    }, { offset: Number.NEGATIVE_INFINITY }).element;
}
