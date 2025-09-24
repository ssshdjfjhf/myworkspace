#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
常见异步编程陷阱和最佳实践
展示异步编程中容易犯的错误和正确的解决方案
"""

import asyncio
import time
import aiohttp
from datetime import datetime
import warnings

def print_time(label):
    """打印当前时间的辅助函数"""
    current_time = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(f"[{current_time}] {label}")

# ==================== 陷阱1: 忘记使用await ====================
async def trap1_missing_await():
    """陷阱1: 忘记使用await关键字"""
    print("=" * 60)
    print("陷阱1: 忘记使用await关键字")
    print("=" * 60)

    async def async_operation():
        await asyncio.sleep(1)
        return "异步操作完成"

    print("\n❌ 错误示例 - 忘记await:")
    start_time = time.time()

    # 错误：忘记await，返回的是协程对象而不是结果
    result = async_operation()  # 这里应该用 await
    print(f"结果类型: {type(result)}")
    print(f"结果内容: {result}")

    # 清理协程对象，避免警告
    result.close()

    end_time = time.time()
    print(f"执行时间: {end_time - start_time:.2f}s (几乎为0，因为没有真正执行)")

    print("\n✅ 正确示例 - 使用await:")
    start_time = time.time()

    # 正确：使用await等待异步操作完成
    result = await async_operation()
    print(f"结果类型: {type(result)}")
    print(f"结果内容: {result}")

    end_time = time.time()
    print(f"执行时间: {end_time - start_time:.2f}s")

# ==================== 陷阱2: 在异步函数中使用阻塞操作 ====================
async def trap2_blocking_operations():
    """陷阱2: 在异步函数中使用阻塞操作"""
    print("\n" + "=" * 60)
    print("陷阱2: 在异步函数中使用阻塞操作")
    print("=" * 60)

    print("\n❌ 错误示例 - 使用阻塞操作:")

    async def bad_async_function():
        print_time("开始执行异步函数")
        # 错误：使用time.sleep会阻塞整个事件循环
        time.sleep(2)  # 这会阻塞所有其他异步任务！
        print_time("异步函数完成")
        return "阻塞操作结果"

    async def other_task():
        for i in range(3):
            print_time(f"其他任务执行 {i+1}")
            await asyncio.sleep(0.5)

    start_time = time.time()
    # 并发执行两个任务
    results = await asyncio.gather(
        bad_async_function(),
        other_task()
    )
    end_time = time.time()
    print(f"总执行时间: {end_time - start_time:.2f}s")
    print("注意：其他任务被阻塞了！")

    print("\n✅ 正确示例 - 使用非阻塞操作:")

    async def good_async_function():
        print_time("开始执行异步函数")
        # 正确：使用asyncio.sleep不会阻塞事件循环
        await asyncio.sleep(2)
        print_time("异步函数完成")
        return "非阻塞操作结果"

    start_time = time.time()
    # 并发执行两个任务
    results = await asyncio.gather(
        good_async_function(),
        other_task()
    )
    end_time = time.time()
    print(f"总执行时间: {end_time - start_time:.2f}s")
    print("注意：两个任务真正并发执行！")

# ==================== 陷阱3: 不正确的异常处理 ====================
async def trap3_exception_handling():
    """陷阱3: 不正确的异常处理"""
    print("\n" + "=" * 60)
    print("陷阱3: 不正确的异常处理")
    print("=" * 60)

    async def failing_task(task_id, should_fail=False):
        await asyncio.sleep(0.5)
        if should_fail:
            raise ValueError(f"任务 {task_id} 失败了！")
        return f"任务 {task_id} 成功完成"

    print("\n❌ 错误示例 - 没有异常处理:")
    try:
        # 如果有任务失败，整个gather会失败
        results = await asyncio.gather(
            failing_task(1, False),
            failing_task(2, True),   # 这个任务会失败
            failing_task(3, False)
        )
        print(f"结果: {results}")
    except Exception as e:
        print(f"捕获异常: {e}")
        print("问题：一个任务失败导致所有任务都被取消")

    print("\n✅ 正确示例1 - 使用return_exceptions:")
    # 使用return_exceptions=True，异常会作为结果返回
    results = await asyncio.gather(
        failing_task(1, False),
        failing_task(2, True),
        failing_task(3, False),
        return_exceptions=True
    )

    print("结果:")
    for i, result in enumerate(results, 1):
        if isinstance(result, Exception):
            print(f"  任务 {i}: 异常 - {result}")
        else:
            print(f"  任务 {i}: 成功 - {result}")

    print("\n✅ 正确示例2 - 单独处理每个任务:")
    async def safe_task(task_id, should_fail=False):
        try:
            return await failing_task(task_id, should_fail)
        except Exception as e:
            return f"任务 {task_id} 异常: {e}"

    results = await asyncio.gather(
        safe_task(1, False),
        safe_task(2, True),
        safe_task(3, False)
    )

    print("结果:")
    for result in results:
        print(f"  {result}")

# ==================== 陷阱4: 资源泄漏 ====================
async def trap4_resource_leaks():
    """陷阱4: 资源泄漏"""
    print("\n" + "=" * 60)
    print("陷阱4: 资源泄漏")
    print("=" * 60)

    print("\n❌ 错误示例 - 没有正确关闭资源:")

    async def bad_http_requests():
        # 错误：没有使用上下文管理器，可能导致连接泄漏
        session = aiohttp.ClientSession()
        try:
            async with session.get('https://httpbin.org/json') as response:
                data = await response.json()
                print(f"获取数据: {data.get('slideshow', {}).get('title', 'N/A')}")
        except Exception as e:
            print(f"请求失败: {e}")
        # 忘记关闭session！这会导致资源泄漏
        # session.close()  # 忘记调用这行

    # 注意：这个示例可能会产生警告
    try:
        await bad_http_requests()
    except Exception as e:
        print(f"执行失败: {e}")

    print("\n✅ 正确示例 - 使用上下文管理器:")

    async def good_http_requests():
        # 正确：使用async with自动管理资源
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get('https://httpbin.org/json') as response:
                    data = await response.json()
                    print(f"获取数据: {data.get('slideshow', {}).get('title', 'N/A')}")
            except Exception as e:
                print(f"请求失败: {e}")
        # session会自动关闭

    try:
        await good_http_requests()
    except Exception as e:
        print(f"网络请求失败（可能是网络问题）: {e}")

# ==================== 陷阱5: 死锁和竞态条件 ====================
async def trap5_deadlocks_and_race_conditions():
    """陷阱5: 死锁和竞态条件"""
    print("\n" + "=" * 60)
    print("陷阱5: 死锁和竞态条件")
    print("=" * 60)

    # 共享资源
    shared_counter = 0
    lock1 = asyncio.Lock()
    lock2 = asyncio.Lock()

    print("\n❌ 错误示例 - 可能的死锁:")

    async def task_a():
        async with lock1:
            print_time("任务A获得锁1")
            await asyncio.sleep(0.1)
            # 尝试获取锁2，但任务B可能已经持有锁2并等待锁1
            async with lock2:
                print_time("任务A获得锁2")

    async def task_b():
        async with lock2:
            print_time("任务B获得锁2")
            await asyncio.sleep(0.1)
            # 尝试获取锁1，但任务A可能已经持有锁1并等待锁2
            async with lock1:
                print_time("任务B获得锁1")

    # 这可能导致死锁（在某些情况下）
    try:
        await asyncio.wait_for(
            asyncio.gather(task_a(), task_b()),
            timeout=2.0
        )
        print("任务完成，没有死锁")
    except asyncio.TimeoutError:
        print("检测到可能的死锁！")

    print("\n✅ 正确示例 - 避免死锁:")

    # 重新创建锁
    lock1 = asyncio.Lock()
    lock2 = asyncio.Lock()

    async def safe_task_a():
        # 总是按相同顺序获取锁
        async with lock1:
            print_time("安全任务A获得锁1")
            async with lock2:
                print_time("安全任务A获得锁2")
                await asyncio.sleep(0.1)

    async def safe_task_b():
        # 总是按相同顺序获取锁
        async with lock1:
            print_time("安全任务B获得锁1")
            async with lock2:
                print_time("安全任务B获得锁2")
                await asyncio.sleep(0.1)

    await asyncio.gather(safe_task_a(), safe_task_b())
    print("安全任务完成，无死锁")

    print("\n竞态条件示例:")

    shared_counter = 0
    counter_lock = asyncio.Lock()

    async def unsafe_increment():
        """不安全的计数器增加"""
        global shared_counter
        for _ in range(1000):
            # 竞态条件：多个任务同时修改shared_counter
            temp = shared_counter
            await asyncio.sleep(0)  # 让出控制权
            shared_counter = temp + 1

    async def safe_increment():
        """安全的计数器增加"""
        global shared_counter
        for _ in range(1000):
            async with counter_lock:
                temp = shared_counter
                await asyncio.sleep(0)
                shared_counter = temp + 1

    # 不安全的并发操作
    shared_counter = 0
    await asyncio.gather(*[unsafe_increment() for _ in range(3)])
    print(f"不安全操作结果: {shared_counter} (期望: 3000)")

    # 安全的并发操作
    shared_counter = 0
    await asyncio.gather(*[safe_increment() for _ in range(3)])
    print(f"安全操作结果: {shared_counter} (期望: 3000)")

# ==================== 陷阱6: 不当的任务创建 ====================
async def trap6_improper_task_creation():
    """陷阱6: 不当的任务创建"""
    print("\n" + "=" * 60)
    print("陷阱6: 不当的任务创建")
    print("=" * 60)

    async def background_task(name, duration):
        print_time(f"后台任务 {name} 开始")
        await asyncio.sleep(duration)
        print_time(f"后台任务 {name} 完成")
        return f"任务 {name} 结果"

    print("\n❌ 错误示例 - 创建任务但不等待:")

    # 错误：创建任务但不等待，可能导致任务被垃圾回收
    task1 = asyncio.create_task(background_task("A", 1))
    task2 = asyncio.create_task(background_task("B", 2))

    # 立即返回，不等待任务完成
    print("主函数继续执行...")
    await asyncio.sleep(0.5)
    print("主函数即将结束...")

    # 任务可能还在运行，但我们没有等待它们
    # 这可能导致警告或任务被取消

    # 清理任务
    task1.cancel()
    task2.cancel()
    try:
        await task1
    except asyncio.CancelledError:
        pass
    try:
        await task2
    except asyncio.CancelledError:
        pass

    print("\n✅ 正确示例1 - 等待所有任务:")

    task1 = asyncio.create_task(background_task("C", 1))
    task2 = asyncio.create_task(background_task("D", 2))

    print("等待所有任务完成...")
    results = await asyncio.gather(task1, task2)
    print(f"任务结果: {results}")

    print("\n✅ 正确示例2 - 使用TaskGroup (Python 3.11+):")

    try:
        # Python 3.11+ 的新特性
        async with asyncio.TaskGroup() as tg:
            task1 = tg.create_task(background_task("E", 1))
            task2 = tg.create_task(background_task("F", 2))

        print(f"TaskGroup结果: {task1.result()}, {task2.result()}")
    except AttributeError:
        print("TaskGroup需要Python 3.11+，跳过此示例")

# ==================== 最佳实践总结 ====================
async def best_practices_summary():
    """最佳实践总结"""
    print("\n" + "=" * 60)
    print("异步编程最佳实践总结")
    print("=" * 60)

    practices = [
        "1. 始终在异步函数调用前使用await",
        "2. 避免在异步函数中使用阻塞操作（如time.sleep）",
        "3. 使用asyncio.sleep而不是time.sleep",
        "4. 正确处理异常，考虑使用return_exceptions=True",
        "5. 使用async with管理资源，避免资源泄漏",
        "6. 避免死锁，按固定顺序获取锁",
        "7. 使用锁保护共享资源，避免竞态条件",
        "8. 创建的任务要么等待完成，要么正确取消",
        "9. 使用asyncio.gather()并发执行多个任务",
        "10. 考虑使用信号量限制并发数量",
        "11. 使用asyncio.wait_for()设置超时",
        "12. 定期让出控制权（await asyncio.sleep(0)）"
    ]

    print("\n异步编程最佳实践:")
    for practice in practices:
        print(f"  {practice}")

    print("\n常用异步编程模式:")
    patterns = [
        "• 生产者-消费者模式：使用asyncio.Queue",
        "• 限流模式：使用asyncio.Semaphore",
        "• 超时模式：使用asyncio.wait_for",
        "• 重试模式：结合异常处理和循环",
        "• 批处理模式：收集任务后批量执行"
    ]

    for pattern in patterns:
        print(f"  {pattern}")

if __name__ == "__main__":
    print("常见异步编程陷阱和最佳实践")
    print()

    async def main():
        # 演示各种陷阱
        await trap1_missing_await()
        await trap2_blocking_operations()
        await trap3_exception_handling()
        await trap4_resource_leaks()
        await trap5_deadlocks_and_race_conditions()
        await trap6_improper_task_creation()

        # 最佳实践总结
        await best_practices_summary()

        print("\n" + "=" * 60)
        print("记住：异步编程的核心是非阻塞和并发")
        print("避免这些常见陷阱，遵循最佳实践，")
        print("可以写出高效、稳定的异步代码！")
        print("=" * 60)

    # 运行主函数
    asyncio.run(main())
