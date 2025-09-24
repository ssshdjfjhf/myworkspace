#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
异步 vs 实时概念对比示例
详细解释异步编程和实时系统的区别
"""

import asyncio
import time
import threading
from datetime import datetime
from queue import Queue
import concurrent.futures

def print_time(label):
    """打印当前时间的辅助函数"""
    current_time = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(f"[{current_time}] {label}")

# ==================== 异步编程示例 ====================
class AsyncTaskManager:
    """异步任务管理器 - 展示异步编程特点"""

    def __init__(self):
        self.tasks = []
        self.results = []

    async def add_task(self, name, duration, priority=1):
        """添加异步任务"""
        task_info = {
            'name': name,
            'duration': duration,
            'priority': priority,
            'created_at': time.time()
        }
        self.tasks.append(task_info)
        print_time(f"异步任务已添加: {name} (预计耗时: {duration}s)")

    async def execute_task(self, task_info):
        """执行单个异步任务"""
        name = task_info['name']
        duration = task_info['duration']

        print_time(f"异步任务开始执行: {name}")
        start_time = time.time()

        # 模拟异步I/O操作（不阻塞其他任务）
        await asyncio.sleep(duration)

        end_time = time.time()
        actual_duration = end_time - start_time

        result = {
            'name': name,
            'planned_duration': duration,
            'actual_duration': actual_duration,
            'completed_at': end_time
        }

        print_time(f"异步任务完成: {name} (实际耗时: {actual_duration:.2f}s)")
        return result

    async def run_all_tasks_concurrent(self):
        """并发执行所有异步任务"""
        print_time("开始并发执行所有异步任务")
        start_time = time.time()

        # 创建所有任务的协程
        coroutines = [self.execute_task(task) for task in self.tasks]

        # 并发执行所有任务
        results = await asyncio.gather(*coroutines)

        end_time = time.time()
        total_time = end_time - start_time

        print_time(f"所有异步任务完成，总耗时: {total_time:.2f}s")
        return results

    async def run_all_tasks_sequential(self):
        """顺序执行所有异步任务"""
        print_time("开始顺序执行所有异步任务")
        start_time = time.time()

        results = []
        for task in self.tasks:
            result = await self.execute_task(task)
            results.append(result)

        end_time = time.time()
        total_time = end_time - start_time

        print_time(f"所有异步任务完成，总耗时: {total_time:.2f}s")
        return results

# ==================== 实时系统模拟示例 ====================
class RealTimeTaskManager:
    """实时任务管理器 - 展示实时系统特点"""

    def __init__(self):
        self.tasks = Queue()
        self.results = []
        self.running = False
        self.worker_threads = []

    def add_task(self, name, duration, deadline, priority=1):
        """添加实时任务"""
        task_info = {
            'name': name,
            'duration': duration,
            'deadline': deadline,  # 截止时间（秒）
            'priority': priority,
            'created_at': time.time()
        }
        self.tasks.put(task_info)
        print_time(f"实时任务已添加: {name} (截止时间: {deadline}s后)")

    def execute_task(self, task_info):
        """执行单个实时任务"""
        name = task_info['name']
        duration = task_info['duration']
        deadline = task_info['deadline']
        created_at = task_info['created_at']

        print_time(f"实时任务开始执行: {name}")
        start_time = time.time()

        # 检查是否已经超过截止时间
        elapsed_since_creation = start_time - created_at
        if elapsed_since_creation > deadline:
            print_time(f"实时任务 {name} 已超过截止时间，跳过执行")
            return {
                'name': name,
                'status': 'missed_deadline',
                'elapsed_time': elapsed_since_creation
            }

        # 模拟实时任务执行（使用真实的阻塞操作）
        time.sleep(duration)

        end_time = time.time()
        total_elapsed = end_time - created_at

        # 检查是否在截止时间内完成
        status = 'completed' if total_elapsed <= deadline else 'deadline_exceeded'

        result = {
            'name': name,
            'status': status,
            'duration': duration,
            'total_elapsed': total_elapsed,
            'deadline': deadline,
            'completed_at': end_time
        }

        print_time(f"实时任务完成: {name} (状态: {status}, 总耗时: {total_elapsed:.2f}s)")
        return result

    def worker(self, worker_id):
        """工作线程"""
        print_time(f"实时工作线程 {worker_id} 启动")

        while self.running:
            try:
                # 获取任务（阻塞等待）
                task = self.tasks.get(timeout=1)
                result = self.execute_task(task)
                self.results.append(result)
                self.tasks.task_done()
            except:
                continue  # 超时或其他异常，继续循环

        print_time(f"实时工作线程 {worker_id} 停止")

    def start_workers(self, num_workers=2):
        """启动工作线程"""
        self.running = True
        for i in range(num_workers):
            thread = threading.Thread(target=self.worker, args=(i+1,))
            thread.start()
            self.worker_threads.append(thread)
        print_time(f"启动了 {num_workers} 个实时工作线程")

    def stop_workers(self):
        """停止工作线程"""
        self.running = False
        for thread in self.worker_threads:
            thread.join()
        print_time("所有实时工作线程已停止")

# ==================== 对比示例 ====================
async def demonstrate_async_vs_realtime():
    """演示异步编程 vs 实时系统的区别"""
    print("=" * 80)
    print("异步编程 vs 实时系统对比示例")
    print("=" * 80)

    # ==================== 异步编程示例 ====================
    print("\n" + "=" * 40)
    print("1. 异步编程示例")
    print("=" * 40)
    print("特点：")
    print("- 非阻塞I/O操作")
    print("- 单线程并发")
    print("- 任务可以并发执行")
    print("- 重点是提高吞吐量和资源利用率")
    print()

    async_manager = AsyncTaskManager()

    # 添加异步任务
    await async_manager.add_task("数据库查询", 2.0)
    await async_manager.add_task("API调用", 1.5)
    await async_manager.add_task("文件处理", 1.0)
    await async_manager.add_task("缓存更新", 0.5)

    print("\n--- 异步并发执行 ---")
    async_concurrent_results = await async_manager.run_all_tasks_concurrent()

    print("\n--- 异步顺序执行 ---")
    async_manager.tasks = [  # 重置任务列表
        {'name': '数据库查询', 'duration': 2.0, 'priority': 1},
        {'name': 'API调用', 'duration': 1.5, 'priority': 1},
        {'name': '文件处理', 'duration': 1.0, 'priority': 1},
        {'name': '缓存更新', 'duration': 0.5, 'priority': 1}
    ]
    async_sequential_results = await async_manager.run_all_tasks_sequential()

    # ==================== 实时系统示例 ====================
    print("\n" + "=" * 40)
    print("2. 实时系统示例")
    print("=" * 40)
    print("特点：")
    print("- 有严格的时间约束")
    print("- 任务必须在截止时间内完成")
    print("- 重点是满足时间要求")
    print("- 通常使用多线程或多进程")
    print()

    realtime_manager = RealTimeTaskManager()
    realtime_manager.start_workers(2)

    # 添加实时任务（带截止时间）
    realtime_manager.add_task("传感器数据处理", 1.0, 2.0)  # 2秒内完成
    realtime_manager.add_task("控制信号发送", 0.5, 1.0)    # 1秒内完成
    realtime_manager.add_task("状态监控", 1.5, 3.0)        # 3秒内完成
    realtime_manager.add_task("紧急响应", 0.3, 0.5)        # 0.5秒内完成

    # 等待任务完成
    await asyncio.sleep(5)
    realtime_manager.stop_workers()

    # ==================== 结果分析 ====================
    print("\n" + "=" * 40)
    print("3. 结果分析")
    print("=" * 40)

    print("\n异步编程结果:")
    concurrent_total = sum(r['actual_duration'] for r in async_concurrent_results)
    sequential_total = sum(r['actual_duration'] for r in async_sequential_results)
    print(f"- 并发执行总时间: {max(r['actual_duration'] for r in async_concurrent_results):.2f}s")
    print(f"- 顺序执行总时间: {sequential_total:.2f}s")
    print(f"- 并发效率提升: {(sequential_total / max(r['actual_duration'] for r in async_concurrent_results)):.1f}x")

    print("\n实时系统结果:")
    completed_tasks = [r for r in realtime_manager.results if r['status'] == 'completed']
    missed_tasks = [r for r in realtime_manager.results if r['status'] == 'missed_deadline']
    exceeded_tasks = [r for r in realtime_manager.results if r['status'] == 'deadline_exceeded']

    print(f"- 按时完成任务: {len(completed_tasks)}")
    print(f"- 错过截止时间: {len(missed_tasks)}")
    print(f"- 超过截止时间: {len(exceeded_tasks)}")
    print(f"- 实时性成功率: {len(completed_tasks) / len(realtime_manager.results) * 100:.1f}%")

# ==================== 概念解释示例 ====================
async def explain_concepts():
    """详细解释异步和实时的概念"""
    print("\n" + "=" * 80)
    print("异步编程 vs 实时系统 - 概念详解")
    print("=" * 80)

    concepts = {
        "异步编程 (Asynchronous Programming)": {
            "定义": "一种编程范式，允许程序在等待某些操作完成时继续执行其他任务",
            "核心特点": [
                "非阻塞I/O操作",
                "单线程并发（通过事件循环）",
                "提高资源利用率和吞吐量",
                "任务执行顺序可能与启动顺序不同"
            ],
            "适用场景": [
                "网络请求处理",
                "文件I/O操作",
                "数据库查询",
                "Web服务器开发"
            ],
            "Python实现": "async/await, asyncio库"
        },

        "实时系统 (Real-time System)": {
            "定义": "必须在指定时间内完成任务的计算机系统，时间约束是系统正确性的一部分",
            "核心特点": [
                "严格的时间约束（截止时间）",
                "可预测的响应时间",
                "任务优先级管理",
                "确定性执行"
            ],
            "适用场景": [
                "工业控制系统",
                "汽车电子系统",
                "医疗设备",
                "航空航天系统"
            ],
            "分类": "硬实时系统（必须满足截止时间）和软实时系统（尽量满足截止时间）"
        }
    }

    for concept_name, details in concepts.items():
        print(f"\n{concept_name}:")
        print(f"定义: {details['定义']}")

        if '核心特点' in details:
            print("核心特点:")
            for feature in details['核心特点']:
                print(f"  • {feature}")

        if '适用场景' in details:
            print("适用场景:")
            for scenario in details['适用场景']:
                print(f"  • {scenario}")

        if 'Python实现' in details:
            print(f"Python实现: {details['Python实现']}")

        if '分类' in details:
            print(f"分类: {details['分类']}")

# ==================== 性能对比示例 ====================
async def performance_comparison():
    """性能对比示例"""
    print("\n" + "=" * 80)
    print("性能对比示例")
    print("=" * 80)

    # 模拟不同类型的任务
    tasks = [
        ("网络请求", 1.0),
        ("数据库查询", 1.5),
        ("文件读取", 0.8),
        ("API调用", 1.2),
        ("数据处理", 0.6)
    ]

    print("\n1. 同步执行（传统方式）:")
    sync_start = time.time()
    for name, duration in tasks:
        print_time(f"开始执行: {name}")
        time.sleep(duration)  # 阻塞执行
        print_time(f"完成执行: {name}")
    sync_end = time.time()
    sync_total = sync_end - sync_start
    print_time(f"同步执行总时间: {sync_total:.2f}s")

    print("\n2. 异步执行:")
    async def async_task(name, duration):
        print_time(f"开始执行: {name}")
        await asyncio.sleep(duration)  # 非阻塞执行
        print_time(f"完成执行: {name}")
        return name

    async_start = time.time()
    async_tasks = [async_task(name, duration) for name, duration in tasks]
    results = await asyncio.gather(*async_tasks)
    async_end = time.time()
    async_total = async_end - async_start
    print_time(f"异步执行总时间: {async_total:.2f}s")

    print("\n3. 多线程执行:")
    def sync_task(name, duration):
        print_time(f"开始执行: {name}")
        time.sleep(duration)
        print_time(f"完成执行: {name}")
        return name

    thread_start = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(sync_task, name, duration) for name, duration in tasks]
        concurrent.futures.wait(futures)
    thread_end = time.time()
    thread_total = thread_end - thread_start
    print_time(f"多线程执行总时间: {thread_total:.2f}s")

    print(f"\n性能对比总结:")
    print(f"- 同步执行: {sync_total:.2f}s (基准)")
    print(f"- 异步执行: {async_total:.2f}s (提升 {sync_total/async_total:.1f}x)")
    print(f"- 多线程执行: {thread_total:.2f}s (提升 {sync_total/thread_total:.1f}x)")

if __name__ == "__main__":
    print("异步编程 vs 实时系统概念对比")
    print()

    async def main():
        # 概念解释
        await explain_concepts()

        # 实际示例对比
        await demonstrate_async_vs_realtime()

        # 性能对比
        await performance_comparison()

        print("\n" + "=" * 80)
        print("总结:")
        print("=" * 80)
        print("异步编程 vs 实时系统的关键区别:")
        print()
        print("1. 目标不同:")
        print("   • 异步编程：提高吞吐量和资源利用率")
        print("   • 实时系统：满足严格的时间约束")
        print()
        print("2. 时间概念:")
        print("   • 异步编程：关注总体执行效率，不保证具体完成时间")
        print("   • 实时系统：必须在指定截止时间内完成任务")
        print()
        print("3. 应用场景:")
        print("   • 异步编程：Web开发、I/O密集型应用")
        print("   • 实时系统：工业控制、嵌入式系统")
        print()
        print("4. 实现方式:")
        print("   • 异步编程：事件循环、协程（async/await）")
        print("   • 实时系统：实时操作系统、优先级调度")
        print("=" * 80)

    # 运行主函数
    asyncio.run(main())
