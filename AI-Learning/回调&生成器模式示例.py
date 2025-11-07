import time

def llm_stream_generator(prompt):
    """模拟大模型的流式生成器函数"""
    # 模拟模型生成的token序列（实际场景中会从大模型API获取）
    tokens = ["你好，", "这是一个", "生成器模式的", "流式输出", "示例。"]
    
    for token in tokens:
        # 模拟模型生成延迟（实际场景中是等待模型返回的时间）
        time.sleep(0.5)
        yield token  # 逐个产出token片段
    
    # 生成结束后返回结束标识
    yield "STREAM_END"

# 调用生成器并消费流式内容
if __name__ == "__main__":
    # 初始化生成器
    stream = llm_stream_generator("请用生成器模式示例演示流式输出")
    
    full_result = []  # 用于拼接完整结果
    
    # 迭代获取每个片段
    for chunk in stream:
        if chunk == "STREAM_END":
            break  # 结束标识，退出循环
        print(f"收到片段：{chunk}")
        full_result.append(chunk)
        print(f"实时显示：{''.join(full_result)}\n")  # 模拟前端实时渲染
        # print("".join(full_result))
    
    # 输出最终完整结果
    print(f"生成完成，完整结果：{''.join(full_result)}")


## 回调模式示例
import time

def llm_stream_with_callback(prompt, on_token, on_complete):
    """模拟大模型流式生成，通过回调函数处理结果"""
    # 模拟模型生成的token序列
    tokens = ["回调模式", "的", "核心是", "异步通知", "，", "每生成一段内容就触发一次回调。"]
    
    full_result = []  # 保存完整结果
    
    for token in tokens:
        # 模拟生成延迟
        time.sleep(0.5)
        full_result.append(token)
        on_token(token)  # 触发片段回调（传递当前token）
    
    # 全部生成完成后触发结束回调
    on_complete(''.join(full_result))

# 定义片段回调函数：处理每个生成的token
def handle_token(token):
    print(f"【片段回调】收到内容：{token}")

# 定义完成回调函数：处理生成结束事件
def handle_complete(full_text):
    print(f"\n【完成回调】生成结束，完整结果：{full_text}")

# 调用流式生成函数，并传入回调函数
if __name__ == "__main__":
    print("开始生成...")
    llm_stream_with_callback(
        prompt="用回调模式演示流式输出",
        on_token=handle_token,  # 注册片段处理回调
        on_complete=handle_complete  # 注册结束处理回调
    )
