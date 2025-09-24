#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网络请求异步示例
对比同步和异步HTTP请求的性能差异
"""

import time
import asyncio
import aiohttp
import requests
from datetime import datetime

def print_time(label):
    """打印当前时间的辅助函数"""
    current_time = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(f"[{current_time}] {label}")

# 测试用的URL列表
URLS = [
    "https://httpbin.org/delay/1",  # 延迟1秒
    "https://httpbin.org/delay/2",  # 延迟2秒
    "https://httpbin.org/delay/1",  # 延迟1秒
    "https://jsonplaceholder.typicode.com/posts/1",
    "https://jsonplaceholder.typicode.com/posts/2",
]

# ==================== 同步网络请求 ====================
def sync_fetch(url):
    """同步获取URL内容"""
    print_time(f"开始请求: {url}")
    try:
        response = requests.get(url, timeout=10)
        print_time(f"完成请求: {url} - 状态码: {response.status_code}")
        return {
            'url': url,
            'status': response.status_code,
            'length': len(response.text)
        }
    except Exception as e:
        print_time(f"请求失败: {url} - 错误: {str(e)}")
        return {'url': url, 'error': str(e)}

def run_sync_requests():
    """运行同步网络请求"""
    print("=" * 60)
    print("同步网络请求示例")
    print("=" * 60)

    start_time = time.time()
    results = []

    for url in URLS:
        result = sync_fetch(url)
        results.append(result)

    end_time = time.time()

    print(f"\n同步请求总耗时: {end_time - start_time:.2f} 秒")
    print(f"成功请求数: {len([r for r in results if 'error' not in r])}")
    return results

# ==================== 异步网络请求 ====================
async def async_fetch(session, url):
    """异步获取URL内容"""
    print_time(f"开始请求: {url}")
    try:
        async with session.get(url, timeout=10) as response:
            content = await response.text()
            print_time(f"完成请求: {url} - 状态码: {response.status}")
            return {
                'url': url,
                'status': response.status,
                'length': len(content)
            }
    except Exception as e:
        print_time(f"请求失败: {url} - 错误: {str(e)}")
        return {'url': url, 'error': str(e)}

async def run_async_requests():
    """运行异步网络请求"""
    print("\n" + "=" * 60)
    print("异步网络请求示例")
    print("=" * 60)

    start_time = time.time()

    # 创建异步HTTP会话
    async with aiohttp.ClientSession() as session:
        # 创建所有任务
        tasks = [async_fetch(session, url) for url in URLS]
        # 并发执行所有任务
        results = await asyncio.gather(*tasks)

    end_time = time.time()

    print(f"\n异步请求总耗时: {end_time - start_time:.2f} 秒")
    print(f"成功请求数: {len([r for r in results if 'error' not in r])}")
    return results

# ==================== 异步请求的不同模式 ====================
async def async_requests_with_semaphore():
    """使用信号量限制并发数的异步请求"""
    print("\n" + "=" * 60)
    print("限制并发数的异步请求示例（最多2个并发）")
    print("=" * 60)

    # 创建信号量，限制最多2个并发请求
    semaphore = asyncio.Semaphore(2)

    async def fetch_with_semaphore(session, url):
        async with semaphore:  # 获取信号量
            return await async_fetch(session, url)

    start_time = time.time()

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_with_semaphore(session, url) for url in URLS]
        results = await asyncio.gather(*tasks)

    end_time = time.time()

    print(f"\n限制并发的异步请求总耗时: {end_time - start_time:.2f} 秒")
    return results

async def async_requests_as_completed():
    """使用as_completed处理异步请求结果"""
    print("\n" + "=" * 60)
    print("使用as_completed处理异步请求")
    print("=" * 60)

    start_time = time.time()

    async with aiohttp.ClientSession() as session:
        tasks = [async_fetch(session, url) for url in URLS]

        # 按完成顺序处理结果
        results = []
        for coro in asyncio.as_completed(tasks):
            result = await coro
            results.append(result)
            print_time(f"收到结果: {result.get('url', 'unknown')}")

    end_time = time.time()

    print(f"\nas_completed 总耗时: {end_time - start_time:.2f} 秒")
    return results

# ==================== 错误处理示例 ====================
async def async_requests_with_error_handling():
    """带错误处理的异步请求示例"""
    print("\n" + "=" * 60)
    print("带错误处理的异步请求示例")
    print("=" * 60)

    # 添加一些会失败的URL
    test_urls = URLS + [
        "https://nonexistent-domain-12345.com",  # 不存在的域名
        "https://httpbin.org/status/500",        # 服务器错误
    ]

    async def safe_fetch(session, url):
        try:
            return await async_fetch(session, url)
        except asyncio.TimeoutError:
            print_time(f"超时: {url}")
            return {'url': url, 'error': 'timeout'}
        except Exception as e:
            print_time(f"异常: {url} - {str(e)}")
            return {'url': url, 'error': str(e)}

    start_time = time.time()

    async with aiohttp.ClientSession() as session:
        tasks = [safe_fetch(session, url) for url in test_urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)

    end_time = time.time()

    print(f"\n带错误处理的异步请求总耗时: {end_time - start_time:.2f} 秒")

    # 统计结果
    success_count = len([r for r in results if isinstance(r, dict) and 'error' not in r])
    error_count = len(results) - success_count

    print(f"成功: {success_count}, 失败: {error_count}")
    return results

if __name__ == "__main__":
    print("网络请求异步编程示例")
    print("需要安装: pip install aiohttp requests")
    print("\n注意：这个示例需要网络连接才能正常运行\n")

    try:
        # 运行同步请求
        sync_results = run_sync_requests()

        # 运行异步请求
        async_results = asyncio.run(run_async_requests())

        # 运行限制并发数的异步请求
        asyncio.run(async_requests_with_semaphore())

        # 运行as_completed示例
        asyncio.run(async_requests_as_completed())

        # 运行错误处理示例
        asyncio.run(async_requests_with_error_handling())

        print("\n" + "=" * 60)
        print("性能对比总结:")
        print("1. 同步请求：按顺序执行，总时间是所有请求时间之和")
        print("2. 异步请求：并发执行，总时间接近最慢请求的时间")
        print("3. 异步编程在I/O密集型任务中优势明显")
        print("4. 可以通过信号量控制并发数，避免过多连接")
        print("=" * 60)

    except ImportError as e:
        print(f"缺少依赖库: {e}")
        print("请运行: pip install aiohttp requests")
    except Exception as e:
        print(f"运行出错: {e}")
        print("请检查网络连接")
