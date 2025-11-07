import openai
from openai import OpenAI
import asyncio
from typing import List, Dict, Any, Generator, AsyncGenerator
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()
    
class DeepSeekClient:
    def __init__(self, api_key: str = None):
        # 如果没有提供 api_key，从环境变量中获取
        if api_key is None:
            api_key = os.environ.get('DEEPSEEK_API_KEY')

        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com"
        )
        self.async_client = openai.AsyncOpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com"
        )

    def chat_completion(self, messages: List[Dict], model: str = "deepseek-chat"):
        """同步聊天完成"""
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.7,
                max_tokens=2000,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )

            return {
                "content": response.choices[0].message.content,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                },
                "model": response.model,
                "finish_reason": response.choices[0].finish_reason
            }

        except openai.RateLimitError as e:
            return {"error": "rate_limit", "message": str(e)}
        except openai.AuthenticationError as e:
            return {"error": "auth", "message": str(e)}
        except Exception as e:
            return {"error": "general", "message": str(e)}

    async def async_chat_completion(self, messages: List[Dict], model: str = "deepseek-chat"):
        """异步聊天完成"""
        try:
            response = await self.async_client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.7,
                max_tokens=2000
            )

            return {
                "content": response.choices[0].message.content,
                "usage": dict(response.usage),
                "model": response.model
            }

        except Exception as e:
            return {"error": str(e)}

    def stream_chat_completion(self, messages: List[Dict], model: str = "deepseek-chat") -> Generator[str, None, None]:
        """生成器模式的流式输出"""
        try:
            stream = self.client.chat.completions.create(
                model=model,
                messages=messages,
                stream=True,
                temperature=0.7
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
        
        except Exception as e:
            yield f"Error: {str(e)}"
    
    def stream_with_callback(self, messages: List[Dict], callback_func, model: str = "deepseek-chat"):
        """回调模式的流式输出"""
        full_response = ""
        
        try:
            stream = self.client.chat.completions.create(
                model=model,
                messages=messages,
                stream=True
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    full_response += content
                    
                    # 调用回调函数
                    callback_func(
                        chunk_content=content,
                        full_content=full_response,
                        chunk_data=chunk
                    )
        
        except Exception as e:
            callback_func(error=str(e))
        
        return full_response
    
    async def async_stream_completion(self, messages: List[Dict], model: str = "deepseek-chat") -> AsyncGenerator[str, None]:
        """异步流式输出"""
        try:
            stream = await self.async_client.chat.completions.create(
                model=model,
                messages=messages,
                stream=True
            )
            
            async for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
        
        except Exception as e:
            yield f"Error: {str(e)}"


# ==================== 使用示例 ====================

if __name__ == "__main__":
    # 创建客户端
    client = DeepSeekClient()

    # print("=" * 50)
    # print("1. 同步调用示例")
    # print("=" * 50)
    # response = client.chat_completion([
    #     {"role": "system", "content": "你是一个有用的AI助手。"},
    #     {"role": "user", "content": "用一句话解释什么是机器学习"}
    # ])
    # print(response)
    # print()
        
    # print("=" * 50)
    # print("2. 流式输出示例（生成器模式）")
    # print("=" * 50)
    # messages = [{"role": "user", "content": "介绍Python的三个优势"}]
    # print("流式输出开始：")
    # for chunk in client.stream_chat_completion(messages):
    #     print(chunk, end='', flush=True)
    # print("\n")

    # print("=" * 50)
    # print("3. 流式输出示例（回调模式）")
    # print("=" * 50)
    # def on_stream_chunk(chunk_content=None, full_content=None, chunk_data=None, error=None):
    #     if error:
    #         print(f"错误: {error}")
    #     else:
    #         print(chunk_content, end='', flush=True)

    # messages = [{"role": "user", "content": "介绍Python的三个优势"}]
    # print("回调模式流式输出：")
    # full_text = client.stream_with_callback(messages, on_stream_chunk)
    # print("\n")
    # print(full_text)

    # print("=" * 50)
    # print("4. 异步调用示例")
    # print("=" * 50)
    # async def async_example():
    #     response = await client.async_chat_completion([
    #         {"role": "user", "content": "什么是深度学习？"}
    #     ])
    #     print("异步调用结果:")
    #     print(response)

    # asyncio.run(async_example())
    # print()

    # print("=" * 50)
    # print("5. 异步流式输出示例")
    # print("=" * 50)
    # async def async_stream_example():
    #     messages = [{"role": "user", "content": "列举5个编程语言"}]
    #     print("异步流式输出：")
    #     async for chunk in client.async_stream_completion(messages):
    #         print(chunk, end='', flush=True)
    #     print()

    # asyncio.run(async_stream_example())



import asyncio
import time

async def async_example():
    # client = DeepSeekClient()
    
    questions = [
        "什么是机器学习？",
        "什么是深度学习？",
        "什么是神经网络？"
    ]
    
    start = time.time()
    
    # 同时发送所有请求
    tasks = [
        client.async_chat_completion([
            {"role": "user", "content": q}
        ])
        for q in questions
    ]
    
    # 等待所有请求完成
    results = await asyncio.gather(*tasks)
    
    print(f"总耗时：{time.time() - start:.1f} 秒")
    return results

asyncio.run(async_example())

# 输出：
# 总耗时：3.0 秒  (3个请求并发执行！)