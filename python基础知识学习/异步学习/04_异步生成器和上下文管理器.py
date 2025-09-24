#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
异步生成器和异步上下文管理器示例
演示 async def 的高级用法
"""

import asyncio
import time
from datetime import datetime
from contextlib import asynccontextmanager

def print_time(label):
    """打印当前时间的辅助函数"""
    current_time = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(f"[{current_time}] {label}")

# ==================== 异步生成器示例 ====================
async def async_number_generator(start, end, delay=0.5):
    """异步数字生成器"""
    print_time(f"异步生成器开始: {start} 到 {end}")

    for i in range(start, end + 1):
        print_time(f"生成数字: {i}")
        yield i
        await asyncio.sleep(delay)  # 模拟异步操作

    print_time("异步生成器结束")

async def async_fibonacci_generator(n, delay=0.3):
    """异步斐波那契数列生成器"""
    print_time(f"开始生成斐波那契数列，前 {n} 项")

    a, b = 0, 1
    count = 0

    while count < n:
        print_time(f"斐波那契数: {a}")
        yield a
        a, b = b, a + b
        count += 1
        await asyncio.sleep(delay)

    print_time("斐波那契生成器结束")

async def async_data_processor():
    """异步数据处理生成器"""
    print_time("数据处理生成器开始")

    # 模拟从不同数据源获取数据
    data_sources = [
        ("数据库", ["用户1", "用户2", "用户3"]),
        ("API", ["订单A", "订单B", "订单C"]),
        ("文件", ["日志1", "日志2", "日志3"])
    ]

    for source_name, data_list in data_sources:
        print_time(f"开始处理 {source_name} 数据")

        for item in data_list:
            # 模拟异步处理时间
            await asyncio.sleep(0.2)
            processed_item = f"[{source_name}处理] {item}"
            print_time(f"处理完成: {processed_item}")
            yield processed_item

        print_time(f"{source_name} 数据处理完成")

    print_time("数据处理生成器结束")

async def demo_async_generators():
    """演示异步生成器的使用"""
    print("=" * 60)
    print("异步生成器示例")
    print("=" * 60)

    # 示例1: 基本异步生成器
    print("\n1. 基本异步生成器:")
    async for num in async_number_generator(1, 5, 0.3):
        print_time(f"接收到数字: {num}")

    # 示例2: 斐波那契异步生成器
    print("\n2. 斐波那契异步生成器:")
    fib_numbers = []
    async for fib in async_fibonacci_generator(6, 0.2):
        fib_numbers.append(fib)
    print_time(f"收集到的斐波那契数列: {fib_numbers}")

    # 示例3: 数据处理异步生成器
    print("\n3. 数据处理异步生成器:")
    processed_data = []
    async for data in async_data_processor():
        processed_data.append(data)
    print_time(f"处理的数据总数: {len(processed_data)}")

# ==================== 异步上下文管理器示例 ====================
class AsyncDatabaseConnection:
    """模拟异步数据库连接"""

    def __init__(self, db_name):
        self.db_name = db_name
        self.connected = False

    async def __aenter__(self):
        """异步进入上下文"""
        print_time(f"正在连接数据库: {self.db_name}")
        await asyncio.sleep(0.5)  # 模拟连接时间
        self.connected = True
        print_time(f"数据库连接成功: {self.db_name}")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步退出上下文"""
        print_time(f"正在关闭数据库连接: {self.db_name}")
        await asyncio.sleep(0.2)  # 模拟关闭时间
        self.connected = False
        print_time(f"数据库连接已关闭: {self.db_name}")

        if exc_type:
            print_time(f"上下文中发生异常: {exc_type.__name__}: {exc_val}")

        return False  # 不抑制异常

    async def query(self, sql):
        """模拟数据库查询"""
        if not self.connected:
            raise RuntimeError("数据库未连接")

        print_time(f"执行查询: {sql}")
        await asyncio.sleep(0.3)  # 模拟查询时间

        # 模拟查询结果
        if "users" in sql.lower():
            result = [{"id": 1, "name": "张三"}, {"id": 2, "name": "李四"}]
        elif "orders" in sql.lower():
            result = [{"id": 101, "amount": 299.99}, {"id": 102, "amount": 199.99}]
        else:
            result = [{"message": "查询完成"}]

        print_time(f"查询结果: {len(result)} 条记录")
        return result

class AsyncFileManager:
    """异步文件管理器"""

    def __init__(self, filename, mode='r'):
        self.filename = filename
        self.mode = mode
        self.file = None

    async def __aenter__(self):
        print_time(f"打开文件: {self.filename}")
        await asyncio.sleep(0.1)  # 模拟文件打开时间

        # 这里简化处理，实际应该使用 aiofiles
        self.file = open(self.filename, self.mode, encoding='utf-8')
        print_time(f"文件已打开: {self.filename}")
        return self.file

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            print_time(f"关闭文件: {self.filename}")
            self.file.close()
            await asyncio.sleep(0.1)  # 模拟文件关闭时间
            print_time(f"文件已关闭: {self.filename}")

# 使用装饰器创建异步上下文管理器
@asynccontextmanager
async def async_timer(name):
    """异步计时器上下文管理器"""
    print_time(f"开始计时: {name}")
    start_time = time.time()

    try:
        yield start_time
    finally:
        end_time = time.time()
        duration = end_time - start_time
        print_time(f"结束计时: {name}, 耗时: {duration:.3f} 秒")

@asynccontextmanager
async def async_resource_pool(resource_name, max_connections=3):
    """异步资源池管理器"""
    print_time(f"初始化资源池: {resource_name} (最大连接数: {max_connections})")

    # 模拟资源池初始化
    pool = {
        'name': resource_name,
        'connections': [],
        'max_connections': max_connections,
        'active_connections': 0
    }

    await asyncio.sleep(0.2)  # 模拟初始化时间
    print_time(f"资源池初始化完成: {resource_name}")

    try:
        yield pool
    finally:
        print_time(f"清理资源池: {resource_name}")
        await asyncio.sleep(0.1)  # 模拟清理时间
        print_time(f"资源池已清理: {resource_name}")

async def demo_async_context_managers():
    """演示异步上下文管理器的使用"""
    print("\n" + "=" * 60)
    print("异步上下文管理器示例")
    print("=" * 60)

    # 示例1: 异步数据库连接
    print("\n1. 异步数据库连接:")
    async with AsyncDatabaseConnection("用户数据库") as db:
        users = await db.query("SELECT * FROM users")
        orders = await db.query("SELECT * FROM orders")

    # 示例2: 异步计时器
    print("\n2. 异步计时器:")
    async with async_timer("数据处理任务") as start_time:
        print_time("执行一些异步任务...")
        await asyncio.sleep(1)
        print_time("任务执行中...")
        await asyncio.sleep(0.5)
        print_time("任务即将完成...")

    # 示例3: 异步资源池
    print("\n3. 异步资源池:")
    async with async_resource_pool("Redis连接池", 5) as pool:
        print_time(f"使用资源池: {pool['name']}")
        await asyncio.sleep(0.5)
        print_time("资源池操作完成")

    # 示例4: 嵌套异步上下文管理器
    print("\n4. 嵌套异步上下文管理器:")
    async with async_timer("嵌套操作"):
        async with AsyncDatabaseConnection("订单数据库") as db1:
            async with AsyncDatabaseConnection("库存数据库") as db2:
                print_time("同时使用两个数据库连接")
                await db1.query("SELECT * FROM orders WHERE status='pending'")
                await db2.query("SELECT * FROM inventory WHERE stock > 0")

# ==================== 异步迭代器示例 ====================
class AsyncRange:
    """异步范围迭代器"""

    def __init__(self, start, stop, step=1, delay=0.1):
        self.start = start
        self.stop = stop
        self.step = step
        self.delay = delay
        self.current = start

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.current >= self.stop:
            raise StopAsyncIteration

        value = self.current
        self.current += self.step

        print_time(f"异步迭代器产生值: {value}")
        await asyncio.sleep(self.delay)

        return value

async def demo_async_iterators():
    """演示异步迭代器的使用"""
    print("\n" + "=" * 60)
    print("异步迭代器示例")
    print("=" * 60)

    print("\n异步范围迭代器:")
    values = []
    async for value in AsyncRange(0, 5, 1, 0.2):
        values.append(value)

    print_time(f"收集到的值: {values}")

# ==================== 综合示例 ====================
async def comprehensive_async_example():
    """综合异步编程示例"""
    print("\n" + "=" * 60)
    print("综合异步编程示例")
    print("=" * 60)

    async with async_timer("综合示例总时间"):
        # 并发执行多个异步任务
        tasks = [
            process_data_with_context("任务1"),
            process_data_with_context("任务2"),
            process_data_with_context("任务3")
        ]

        results = await asyncio.gather(*tasks)
        print_time(f"所有任务完成，结果数量: {len(results)}")

async def process_data_with_context(task_name):
    """使用上下文管理器处理数据的任务"""
    async with async_timer(f"{task_name}执行时间"):
        async with AsyncDatabaseConnection(f"{task_name}数据库") as db:
            # 使用异步生成器处理数据
            processed_count = 0
            async for num in async_number_generator(1, 3, 0.1):
                await db.query(f"INSERT INTO results VALUES ({num})")
                processed_count += 1

            return f"{task_name}处理了{processed_count}条数据"

if __name__ == "__main__":
    print("异步生成器和异步上下文管理器示例")
    print()

    async def main():
        # 演示异步生成器
        await demo_async_generators()

        # 演示异步上下文管理器
        await demo_async_context_managers()

        # 演示异步迭代器
        await demo_async_iterators()

        # 综合示例
        await comprehensive_async_example()

        print("\n" + "=" * 60)
        print("异步生成器和上下文管理器总结:")
        print("1. 异步生成器使用 async def + yield")
        print("2. 异步上下文管理器实现 __aenter__ 和 __aexit__")
        print("3. @asynccontextmanager 装饰器简化上下文管理器创建")
        print("4. 异步迭代器实现 __aiter__ 和 __anext__")
        print("5. 这些特性让异步代码更加优雅和强大")
        print("=" * 60)

    # 运行主函数
    asyncio.run(main())
