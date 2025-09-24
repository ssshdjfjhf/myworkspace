#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件I/O异步示例
演示同步和异步文件操作的差异
"""

import os
import time
import asyncio
import aiofiles
from datetime import datetime
from pathlib import Path

def print_time(label):
    """打印当前时间的辅助函数"""
    current_time = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(f"[{current_time}] {label}")

# 创建测试目录
TEST_DIR = Path(__file__).parent / "test_files"
TEST_DIR.mkdir(exist_ok=True)

# ==================== 同步文件操作 ====================
def sync_write_file(filename, content, delay=0):
    """同步写入文件"""
    filepath = TEST_DIR / filename
    print_time(f"开始写入文件: {filename}")

    if delay:
        time.sleep(delay)  # 模拟处理时间

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print_time(f"完成写入文件: {filename}")
    return filepath

def sync_read_file(filename, delay=0):
    """同步读取文件"""
    filepath = TEST_DIR / filename
    print_time(f"开始读取文件: {filename}")

    if delay:
        time.sleep(delay)  # 模拟处理时间

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        print_time(f"完成读取文件: {filename} (长度: {len(content)})")
        return content
    except FileNotFoundError:
        print_time(f"文件不存在: {filename}")
        return None

def run_sync_file_operations():
    """运行同步文件操作"""
    print("=" * 60)
    print("同步文件操作示例")
    print("=" * 60)

    start_time = time.time()

    # 创建测试文件内容
    files_to_create = [
        ("sync_file1.txt", "这是同步文件1的内容\n" * 100, 0.5),
        ("sync_file2.txt", "这是同步文件2的内容\n" * 200, 0.3),
        ("sync_file3.txt", "这是同步文件3的内容\n" * 150, 0.4),
    ]

    # 同步写入文件
    created_files = []
    for filename, content, delay in files_to_create:
        filepath = sync_write_file(filename, content, delay)
        created_files.append(filename)

    # 同步读取文件
    read_results = []
    for filename in created_files:
        content = sync_read_file(filename, 0.2)
        read_results.append((filename, len(content) if content else 0))

    end_time = time.time()

    print(f"\n同步文件操作总耗时: {end_time - start_time:.2f} 秒")
    print(f"处理文件数: {len(created_files)}")
    for filename, length in read_results:
        print(f"  {filename}: {length} 字符")

    return created_files

# ==================== 异步文件操作 ====================
async def async_write_file(filename, content, delay=0):
    """异步写入文件"""
    filepath = TEST_DIR / filename
    print_time(f"开始写入文件: {filename}")

    if delay:
        await asyncio.sleep(delay)  # 模拟异步处理时间

    async with aiofiles.open(filepath, 'w', encoding='utf-8') as f:
        await f.write(content)

    print_time(f"完成写入文件: {filename}")
    return filepath

async def async_read_file(filename, delay=0):
    """异步读取文件"""
    filepath = TEST_DIR / filename
    print_time(f"开始读取文件: {filename}")

    if delay:
        await asyncio.sleep(delay)  # 模拟异步处理时间

    try:
        async with aiofiles.open(filepath, 'r', encoding='utf-8') as f:
            content = await f.read()
        print_time(f"完成读取文件: {filename} (长度: {len(content)})")
        return content
    except FileNotFoundError:
        print_time(f"文件不存在: {filename}")
        return None

async def run_async_file_operations():
    """运行异步文件操作"""
    print("\n" + "=" * 60)
    print("异步文件操作示例")
    print("=" * 60)

    start_time = time.time()

    # 创建测试文件内容
    files_to_create = [
        ("async_file1.txt", "这是异步文件1的内容\n" * 100, 0.5),
        ("async_file2.txt", "这是异步文件2的内容\n" * 200, 0.3),
        ("async_file3.txt", "这是异步文件3的内容\n" * 150, 0.4),
    ]

    # 异步并发写入文件
    write_tasks = [
        async_write_file(filename, content, delay)
        for filename, content, delay in files_to_create
    ]
    created_files = await asyncio.gather(*write_tasks)

    # 异步并发读取文件
    filenames = [filename for filename, _, _ in files_to_create]
    read_tasks = [async_read_file(filename, 0.2) for filename in filenames]
    read_contents = await asyncio.gather(*read_tasks)

    end_time = time.time()

    print(f"\n异步文件操作总耗时: {end_time - start_time:.2f} 秒")
    print(f"处理文件数: {len(filenames)}")
    for filename, content in zip(filenames, read_contents):
        length = len(content) if content else 0
        print(f"  {filename}: {length} 字符")

    return filenames

# ==================== 大文件处理示例 ====================
async def async_process_large_file():
    """异步处理大文件示例"""
    print("\n" + "=" * 60)
    print("异步大文件处理示例")
    print("=" * 60)

    large_file = TEST_DIR / "large_file.txt"
    processed_file = TEST_DIR / "processed_large_file.txt"

    # 创建大文件
    print_time("创建大文件...")
    async with aiofiles.open(large_file, 'w', encoding='utf-8') as f:
        for i in range(10000):
            await f.write(f"这是第 {i+1} 行内容，包含一些测试数据。\n")
            if i % 1000 == 0:
                await asyncio.sleep(0)  # 让出控制权

    print_time("大文件创建完成")

    # 异步逐行处理大文件
    print_time("开始处理大文件...")
    start_time = time.time()

    line_count = 0
    async with aiofiles.open(large_file, 'r', encoding='utf-8') as input_file:
        async with aiofiles.open(processed_file, 'w', encoding='utf-8') as output_file:
            async for line in input_file:
                # 模拟处理每一行
                processed_line = f"[处理后] {line.strip()}\n"
                await output_file.write(processed_line)
                line_count += 1

                # 每处理1000行让出一次控制权
                if line_count % 1000 == 0:
                    await asyncio.sleep(0)
                    print_time(f"已处理 {line_count} 行")

    end_time = time.time()
    print_time(f"大文件处理完成，共处理 {line_count} 行，耗时 {end_time - start_time:.2f} 秒")

# ==================== 文件监控示例 ====================
async def async_file_monitor():
    """异步文件监控示例"""
    print("\n" + "=" * 60)
    print("异步文件监控示例")
    print("=" * 60)

    monitor_file = TEST_DIR / "monitor_test.txt"

    async def write_to_file():
        """定期写入文件"""
        for i in range(5):
            await asyncio.sleep(1)
            async with aiofiles.open(monitor_file, 'a', encoding='utf-8') as f:
                await f.write(f"时间戳: {datetime.now()}, 计数: {i+1}\n")
            print_time(f"写入数据 {i+1}")

    async def monitor_file_size():
        """监控文件大小变化"""
        last_size = 0
        for _ in range(6):  # 监控6秒
            await asyncio.sleep(1)
            if monitor_file.exists():
                current_size = monitor_file.stat().st_size
                if current_size != last_size:
                    print_time(f"文件大小变化: {last_size} -> {current_size} 字节")
                    last_size = current_size
                else:
                    print_time("文件大小无变化")
            else:
                print_time("文件不存在")

    # 并发执行写入和监控
    await asyncio.gather(
        write_to_file(),
        monitor_file_size()
    )

# ==================== 批量文件操作 ====================
async def async_batch_file_operations():
    """异步批量文件操作示例"""
    print("\n" + "=" * 60)
    print("异步批量文件操作示例")
    print("=" * 60)

    # 创建多个小文件
    batch_files = [f"batch_file_{i}.txt" for i in range(10)]

    async def create_file(filename):
        content = f"这是批量文件 {filename} 的内容\n" * 50
        await async_write_file(filename, content, 0.1)
        return filename

    async def process_file(filename):
        """处理单个文件：读取、修改、写回"""
        content = await async_read_file(filename)
        if content:
            # 添加处理标记
            processed_content = f"[已处理] {content}"
            new_filename = f"processed_{filename}"
            await async_write_file(new_filename, processed_content)
            return new_filename
        return None

    start_time = time.time()

    # 并发创建文件
    print_time("开始批量创建文件...")
    create_tasks = [create_file(filename) for filename in batch_files]
    created = await asyncio.gather(*create_tasks)

    # 并发处理文件
    print_time("开始批量处理文件...")
    process_tasks = [process_file(filename) for filename in created]
    processed = await asyncio.gather(*process_tasks)

    end_time = time.time()

    successful_processed = [f for f in processed if f is not None]
    print_time(f"批量操作完成，处理了 {len(successful_processed)} 个文件，耗时 {end_time - start_time:.2f} 秒")

def cleanup_test_files():
    """清理测试文件"""
    if TEST_DIR.exists():
        for file in TEST_DIR.glob("*"):
            if file.is_file():
                file.unlink()
        print_time("清理测试文件完成")

if __name__ == "__main__":
    print("文件I/O异步编程示例")
    print("需要安装: pip install aiofiles")
    print()

    try:
        # 运行同步文件操作
        sync_files = run_sync_file_operations()

        # 运行异步文件操作
        asyncio.run(run_async_file_operations())

        # 运行大文件处理示例
        asyncio.run(async_process_large_file())

        # 运行文件监控示例
        asyncio.run(async_file_monitor())

        # 运行批量文件操作示例
        asyncio.run(async_batch_file_operations())

        print("\n" + "=" * 60)
        print("文件I/O异步编程总结:")
        print("1. 异步文件操作可以并发处理多个文件")
        print("2. 大文件处理时要注意让出控制权（await asyncio.sleep(0)）")
        print("3. aiofiles 提供了异步文件操作接口")
        print("4. 异步I/O在处理大量文件时性能优势明显")
        print("=" * 60)

        # 清理测试文件
        cleanup_test_files()

    except ImportError as e:
        print(f"缺少依赖库: {e}")
        print("请运行: pip install aiofiles")
    except Exception as e:
        print(f"运行出错: {e}")
        import traceback
        traceback.print_exc()
