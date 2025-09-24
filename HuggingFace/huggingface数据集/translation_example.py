# 翻译DataFrame指定列的使用示例

# 导入必要的库
import pandas as pd
from translate_helper import DataFrameTranslator, translate_dataframe_column, batch_translate_column

# 假设你已经有了client对象和df数据
# client = ... (你的API客户端)
# df = ... (你的DataFrame)

# 方法1: 使用类的方式（推荐，功能最全）
def example_class_based_translation(df, client):
    """使用DataFrameTranslator类进行翻译"""

    # 创建翻译器实例
    translator = DataFrameTranslator(client, model_name="LongCat-Flash-Chat")

    # 翻译单个列
    # 将'act'列翻译为中文，结果保存在'act_zh'列
    df_translated = translator.translate_column(
        df=df,
        source_column='act',           # 要翻译的列名
        target_column='act_zh',        # 翻译结果列名（可选，默认为源列名_zh）
        max_workers=3,                 # 并发线程数
        batch_size=20                  # 处理前20行
    )

    return df_translated

def example_multiple_columns_translation(df, client):
    """翻译多个列"""

    translator = DataFrameTranslator(client)

    # 定义要翻译的列映射
    column_mapping = {
        'act': 'act_zh',              # 将act列翻译为act_zh
        'description': 'description_zh',  # 将description列翻译为description_zh
        'title': 'title_zh'           # 将title列翻译为title_zh
    }

    # 批量翻译多个列
    df_translated = translator.translate_multiple_columns(
        df=df,
        column_mapping=column_mapping,
        max_workers=3,
        batch_size=50
    )

    return df_translated

# 方法2: 使用便捷函数（简单快速）
def example_simple_function(df, client):
    """使用便捷函数进行翻译"""

    # 翻译指定列
    df_translated = translate_dataframe_column(
        df=df,
        client=client,
        source_column='act',           # 要翻译的列
        target_column='act_chinese',   # 目标列名
        max_workers=3,
        batch_size=20
    )

    return df_translated

# 方法3: 使用批量翻译函数（兼容原代码风格）
def example_batch_function(df, client):
    """使用批量翻译函数"""

    df_translated = batch_translate_column(
        df=df,
        client=client,
        source_column='act',
        target_column='act_zh',
        max_workers=3,
        batch_size=20
    )

    return df_translated

# 方法4: 原始apply方式的优化版本
def example_apply_method(df, client):
    """使用apply方法的优化版本"""
    from translate_helper import get_answer

    # 创建副本
    df_copy = df[:20].copy()

    # 使用apply翻译指定列
    df_copy['act_zh'] = df_copy.apply(
        lambda row: get_answer(row, client, column_name='act'),
        axis=1
    )

    return df_copy

# 实际使用示例
if __name__ == "__main__":
    # 假设你有以下数据和客户端
    # df = pd.read_csv('your_data.csv')  # 你的数据
    # client = YourAPIClient()           # 你的API客户端

    # 示例数据（用于测试）
    sample_data = {
        'act': [
            'Create a detailed project plan',
            'Review the code implementation',
            'Test the new features',
            'Deploy to production environment'
        ],
        'description': [
            'Plan should include timeline and resources',
            'Focus on code quality and best practices',
            'Comprehensive testing of all functionalities',
            'Ensure smooth deployment process'
        ]
    }
    df = pd.DataFrame(sample_data)

    print("原始数据:")
    print(df)
    print("\n" + "="*50 + "\n")

    # 使用不同方法进行翻译（选择其中一种即可）

    # 方法1: 推荐使用
    # df_result = example_class_based_translation(df, client)

    # 方法2: 简单函数
    # df_result = example_simple_function(df, client)

    # 方法3: 批量函数
    # df_result = example_batch_function(df, client)

    # 方法4: Apply方式
    # df_result = example_apply_method(df, client)

    print("翻译后的数据:")
    # print(df_result)

    # 保存结果
    # df_result.to_csv('translated_data.csv', index=False)
    print("请取消注释相应的方法来运行翻译")

# 快速使用模板
"""
# 最简单的使用方式：
from translate_helper import translate_dataframe_column

# 翻译DataFrame中的'act'列为中文
df_translated = translate_dataframe_column(
    df=df,                    # 你的DataFrame
    client=client,            # 你的API客户端
    source_column='act',      # 要翻译的列名
    target_column='act_zh',   # 翻译结果列名（可选）
    batch_size=20            # 处理行数（可选）
)

print(df_translated[['act', 'act_zh']])  # 查看翻译结果
"""
