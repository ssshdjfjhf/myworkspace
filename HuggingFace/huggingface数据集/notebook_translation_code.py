# 在Jupyter Notebook中直接使用的翻译代码
# 复制以下代码到你的notebook单元格中

import pandas as pd
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def translate_text_with_retry(client, text, max_retries=3, model_name="LongCat-Flash-Chat"):
    """
    翻译单个文本，带重试机制
    """
    if pd.isna(text) or text == "":
        return ""

    system_message = {
        "role": "system",
        "content": "你是一名英语翻译专家，请将以下内容翻译为中文，保持原文的语义和语调"
    }

    for attempt in range(max_retries):
        try:
            messages = [
                system_message,
                {"role": "user", "content": str(text)}
            ]

            response = client.chat.completions.create(
                model=model_name,
                messages=messages,
                max_tokens=2048,
                temperature=0.3,
                stream=False
            )

            result = response.choices[0].message.content.strip()
            logger.info(f"翻译成功: {str(text)[:30]}... -> {result[:30]}...")
            return result

        except Exception as e:
            logger.warning(f"翻译失败 (尝试 {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # 指数退避
            else:
                logger.error(f"翻译最终失败: {text[:50]}...")
                return f"[翻译失败: {str(e)}]"

def translate_dataframe_column(df, client, source_column, target_column=None,
                             max_workers=3, batch_size=None, model_name="LongCat-Flash-Chat"):
    """
    翻译DataFrame中指定列的内容

    参数:
        df: 源DataFrame
        client: API客户端
        source_column: 要翻译的列名
        target_column: 翻译结果列名（可选，默认为源列名_zh）
        max_workers: 并发线程数
        batch_size: 处理的行数（可选，默认处理所有行）
        model_name: 使用的模型名称

    返回:
        包含翻译结果的新DataFrame
    """
    # 验证输入
    if source_column not in df.columns:
        raise ValueError(f"列 '{source_column}' 不存在于DataFrame中")

    # 设置目标列名
    if target_column is None:
        target_column = f"{source_column}_zh"

    # 创建副本
    df_result = df.copy()

    # 确定处理范围
    if batch_size is not None:
        df_to_process = df_result.head(batch_size)
    else:
        df_to_process = df_result

    # 获取需要翻译的文本列表
    texts_to_translate = df_to_process[source_column].tolist()
    indices = df_to_process.index.tolist()

    logger.info(f"开始翻译 {len(texts_to_translate)} 条记录...")

    # 并发翻译
    translated_texts = [''] * len(texts_to_translate)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 提交翻译任务
        future_to_index = {
            executor.submit(translate_text_with_retry, client, text, 3, model_name): i
            for i, text in enumerate(texts_to_translate)
        }

        # 收集结果
        completed = 0
        for future in as_completed(future_to_index):
            idx = future_to_index[future]
            try:
                result = future.result()
                translated_texts[idx] = result
                completed += 1

                # 显示进度
                if completed % 5 == 0 or completed == len(texts_to_translate):
                    logger.info(f"翻译进度: {completed}/{len(texts_to_translate)}")

            except Exception as e:
                logger.error(f"处理第{idx}条记录时出错: {e}")
                translated_texts[idx] = f"[处理失败: {str(e)}]"

    # 将翻译结果添加到DataFrame
    for i, original_idx in enumerate(indices):
        df_result.loc[original_idx, target_column] = translated_texts[i]

    logger.info(f"翻译完成！结果保存在列 '{target_column}' 中")
    return df_result

# 简化版本 - 使用apply方法（适合小数据量）
def simple_translate_column(df, client, source_column, target_column=None, batch_size=20):
    """
    简化版翻译函数，使用apply方法
    """
    if target_column is None:
        target_column = f"{source_column}_zh"

    def translate_single_text(text):
        if pd.isna(text) or text == "":
            return ""

        try:
            messages = [
                {"role": "system", "content": "你是一名英语翻译专家，请将以下内容翻译为中文"},
                {"role": "user", "content": str(text)}
            ]

            response = client.chat.completions.create(
                model="LongCat-Flash-Chat",
                messages=messages,
                max_tokens=2048,
                temperature=0.3,
                stream=False
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            logger.error(f"翻译失败: {e}")
            return f"翻译失败: {str(e)}"

    # 创建副本并翻译
    df_copy = df.head(batch_size).copy()
    df_copy[target_column] = df_copy[source_column].apply(translate_single_text)

    return df_copy

# 使用示例：
"""
# 方法1: 推荐使用（支持并发，效率高）
df_translated = translate_dataframe_column(
    df=df,                      # 你的DataFrame
    client=client,              # 你的API客户端
    source_column='act',        # 要翻译的列名
    target_column='act_zh',     # 翻译结果列名
    max_workers=3,              # 并发线程数
    batch_size=20               # 处理前20行
)

# 方法2: 简化版本（适合小数据量）
df_translated = simple_translate_column(
    df=df,
    client=client,
    source_column='act',
    target_column='act_zh',
    batch_size=20
)

# 查看结果
print(df_translated[['act', 'act_zh']])

# 保存结果
df_translated.to_csv('translated_data.csv', index=False)
"""

print("翻译工具已加载完成！")
print("使用方法：")
print("1. translate_dataframe_column() - 推荐使用，支持并发")
print("2. simple_translate_column() - 简化版本，适合小数据量")
print("\n请参考代码末尾的使用示例")
