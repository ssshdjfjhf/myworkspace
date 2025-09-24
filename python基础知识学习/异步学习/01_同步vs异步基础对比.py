#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
同步 vs 异步基础对比示例
演示同步和异步函数的基本差异
"""

import time
import asyncio
from datetime import datetime

def print_time(label):
    """打印当前时间的辅助函数"""
    current_time = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(f"[{current_time}] {label}")

# ==================== 同步函数示例 ====================
def sync_task(name, duration):
    """同步任务 - 会阻塞执行"""
    print_time(f"同步任务 {name} 开始")
    time.sleep(duration)  # 模拟耗时操作（阻塞）
    print_time(f"同步任务 {name} 完成")
    return f"同步任务 {name} 的结果"

def run_sync_tasks():
    """运行多个同步任务"""
    print("=" * 50)
    print("运行同步任务（串行执行）")
    print("=" * 50)

    start_time = time.time()

    # 同步执行多个任务 - 串行执行
    result1 = sync_task("A", 2)
    result2 = sync_task("B", 1)
    result3 = sync_task("C", 1.5)

    end_time = time.time()
    print(f"\n同步任务总耗时: {end_time - start_time:.2f} 秒")
    print(f"结果: {[result1, result2, result3]}")

# ==================== 异步函数示例 ====================
async def async_task(name, duration):
    """异步任务 - 不会阻塞执行"""
    print_time(f"异步任务 {name} 开始")
    await asyncio.sleep(duration)  # 模拟耗时操作（非阻塞）
    print_time(f"异步任务 {name} 完成")
    return f"异步任务 {name} 的结果"

async def run_async_tasks():
    """运行多个异步任务"""
    print("\n" + "=" * 50)
    print("运行异步任务（并发执行）")
    print("=" * 50)

    start_time = time.time()

    # 异步并发执行多个任务
    tasks = [
        async_task("A", 2),
        async_task("B", 1),
        async_task("C", 1.5)
    ]

    results = await asyncio.gather(*tasks)

    end_time = time.time()
    print(f"\n异步任务总耗时: {end_time - start_time:.2f} 秒")
    print(f"结果: {results}")

# ==================== 混合示例 ====================
async def mixed_example():
    """混合使用同步和异步的示例"""
    print("\n" + "=" * 50)
    print("混合示例：在异步函数中调用同步操作")
    print("=" * 50)

    print_time("异步函数开始")

    # 在异步函数中执行同步操作
    print_time("执行同步操作前")
    time.sleep(1)  # 这会阻塞整个事件循环！
    print_time("执行同步操作后")

    # 正确的异步操作
    print_time("执行异步操作前")
    await asyncio.sleep(1)  # 这不会阻塞事件循环
    print_time("执行异步操作后")

if __name__ == "__main__":
    print("Python 异步编程基础对比示例")
    print("观察执行时间和顺序的差异\n")

    # 运行同步任务
    run_sync_tasks()

    # 运行异步任务
    asyncio.run(run_async_tasks())

    # 运行混合示例
    asyncio.run(mixed_example())

    print("\n" + "=" * 50)
    print("总结:")
    print("1. 同步任务按顺序执行，总时间是各任务时间之和")
    print("2. 异步任务可以并发执行，总时间接近最长任务的时间")
    print("3. async/await 是 Python 异步编程的关键字")
    print("=" * 50)
