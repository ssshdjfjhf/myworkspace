import pandas as pd
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from typing import Optional, List, Union

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DataFrameTranslator:
    """DataFrame翻译器类"""

    def __init__(self, client, model_name="LongCat-Flash-Chat"):
        """
        初始化翻译器

        Args:
            client: API客户端对象
            model_name: 使用的模型名称
        """
        self.client = client
        self.model_name = model_name
        self.system_message = {
            "role": "system",
            "content": "你是一名英语翻译专家，请将以下内容翻译为中文，保持原文的语义和语调"
        }

    def translate_text(self, text: str, max_retries: int = 3) -> str:
        """
        翻译单个文本

        Args:
            text: 要翻译的文本
            max_retries: 最大重试次数

        Returns:
            翻译后的中文文本
        """
        if pd.isna(text) or text == "":
            return ""

        for attempt in range(max_retries):
            try:
                messages = [
                    self.system_message,
                    {"role": "user", "content": str(text)}
                ]

                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=messages,
                    max_tokens=2048,
                    temperature=0.3,  # 降低温度以获得更一致的翻译
                    stream=False
                )

                result = response.choices[0].message.content.strip()
                logger.info(f"翻译成功: {str(text)[:50]}... -> {result[:50]}...")
                return result

            except Exception as e:
                logger.warning(f"翻译失败 (尝试 {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # 指数退避
                else:
                    logger.error(f"翻译最终失败: {text[:100]}...")
                    return f"[翻译失败: {str(e)}]"

    def translate_column(self,
                        df: pd.DataFrame,
                        source_column: str,
                        target_column: Optional[str] = None,
                        max_workers: int = 3,
                        batch_size: Optional[int] = None) -> pd.DataFrame:
        """
        翻译DataFrame中指定列的内容

        Args:
            df: 源DataFrame
            source_column: 要翻译的列名
            target_column: 翻译结果存储的列名，如果为None则为 source_column + '_zh'
            max_workers: 并发线程数
            batch_size: 批处理大小，如果为None则处理所有行

        Returns:
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
                executor.submit(self.translate_text, text): i
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

    def translate_multiple_columns(self,
                                 df: pd.DataFrame,
                                 column_mapping: dict,
                                 max_workers: int = 3,
                                 batch_size: Optional[int] = None) -> pd.DataFrame:
        """
        翻译多个列

        Args:
            df: 源DataFrame
            column_mapping: 列映射字典 {源列名: 目标列名}
            max_workers: 并发线程数
            batch_size: 批处理大小

        Returns:
            包含所有翻译结果的DataFrame
        """
        df_result = df.copy()

        for source_col, target_col in column_mapping.items():
            logger.info(f"开始翻译列: {source_col} -> {target_col}")
            df_result = self.translate_column(
                df_result,
                source_col,
                target_col,
                max_workers=max_workers,
                batch_size=batch_size
            )

        return df_result


# 使用示例函数
def translate_dataframe_column(df, client, source_column, target_column=None,
                             max_workers=3, batch_size=None, model_name="LongCat-Flash-Chat"):
    """
    便捷函数：翻译DataFrame中的指定列

    Args:
        df: 源DataFrame
        client: API客户端
        source_column: 要翻译的列名
        target_column: 目标列名（可选）
        max_workers: 并发数
        batch_size: 批处理大小
        model_name: 模型名称

    Returns:
        翻译后的DataFrame
    """
    translator = DataFrameTranslator(client, model_name)
    return translator.translate_column(df, source_column, target_column, max_workers, batch_size)


# 原代码的优化版本（保持兼容性）
def get_message(text):
    """构建API调用的消息格式"""
    try:
        if pd.isna(text) or text == "":
            return None

        message_list = [
            {"role": "system", "content": "你是一名英语翻译专家，请将以下内容翻译为中文"},
            {"role": "user", "content": str(text)}
        ]
        return message_list
    except Exception as e:
        logger.error(f"构建消息时出错: {e}")
        return None

def get_answer(row, client, column_name='act'):
    """翻译指定列的内容"""
    try:
        if column_name not in row:
            return f"列 '{column_name}' 不存在"

        text = row[column_name]
        messages = get_message(text)

        if messages is None:
            return "消息构建失败"

        response = client.chat.completions.create(
            model="LongCat-Flash-Chat",
            messages=messages,
            max_tokens=2048,
            temperature=0.3,
            stream=False
        )

        result = response.choices[0].message.content.strip()
        return result

    except Exception as e:
        logger.error(f"翻译失败: {e}")
        return f"翻译失败: {str(e)}"

# 批量翻译函数
def batch_translate_column(df, client, source_column, target_column=None,
                          max_workers=3, batch_size=20):
    """
    批量翻译DataFrame中指定列的内容

    Args:
        df: 源DataFrame
        client: API客户端
        source_column: 要翻译的列名
        target_column: 目标列名，默认为 source_column + '_zh'
        max_workers: 并发线程数
        batch_size: 处理的行数

    Returns:
        包含翻译结果的DataFrame
    """
    if target_column is None:
        target_column = f"{source_column}_zh"

    # 使用新的翻译器
    return translate_dataframe_column(
        df, client, source_column, target_column,
        max_workers, batch_size
    )
