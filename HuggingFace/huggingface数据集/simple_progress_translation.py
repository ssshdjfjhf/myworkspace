# 简化版 - 直接在Jupyter Notebook中使用的带进度条翻译代码
# 复制以下代码到你的notebook单元格中

import pandas as pd
import json
from tqdm import tqdm

# 首先确保安装了tqdm
# 如果没有安装，运行: !pip install tqdm

# 你现有的函数（已修复）
def get_message(row):
    try:
        message_list = []
        system_message = {"role": "system", "content": "你是一名英语翻译专家，请将以下内容翻译为中文"}
        message_list.append(system_message)
        user_message = {"role": "user", "content": row['act']}
        message_list.append(user_message)
        return message_list
    except:
        return "调用结果出错"

def get_answer(row):
    try:
        message = get_message(row)
        if message == "调用结果出错":
            return "调用结果出错"

        response = client.chat.completions.create(
            model="LongCat-Flash-Chat",
            messages=message,
            max_tokens=2048,
            temperature=0.5,
            stream=False
        )
        return json.loads(response.to_json())['choices'][0]['message']['content']
    except:
        return "调用结果出错"

# 方法1: 最简单的方式 - 只需要改一行代码！
print("方法1: 使用progress_apply（推荐）")
print("只需要将你的 df.apply() 改为 df.progress_apply() 即可！")
print()

# 启用tqdm的pandas支持
tqdm.pandas(desc="翻译进度")

# 原来的代码: df['act_zh'] = df.apply(get_answer, axis=1)
# 新代码（带进度条）:
# df['act_zh'] = df.progress_apply(get_answer, axis=1)

print("="*60)
print("方法2: 手动循环with进度条（更灵活）")

def translate_with_manual_progress(df, column_name='act', target_column='act_zh'):
    """手动循环with进度条"""
    results = []

    # 创建进度条
    for idx, row in tqdm(df.iterrows(), total=len(df), desc="翻译进度", unit="条"):
        result = get_answer(row)
        results.append(result)

        # 可选：显示当前处理的内容（前30个字符）
        current_text = str(row[column_name])[:30] + "..." if len(str(row[column_name])) > 30 else str(row[column_name])
        tqdm.write(f"正在翻译: {current_text}")

    df[target_column] = results
    return df

print("="*60)
print("方法3: 批量处理with详细进度信息")

def translate_with_detailed_progress(df, column_name='act', target_column='act_zh', batch_size=5):
    """批量处理with详细进度信息"""
    results = []
    success_count = 0
    error_count = 0

    with tqdm(total=len(df), desc="翻译进度", unit="条") as pbar:
        for i in range(0, len(df), batch_size):
            batch_end = min(i + batch_size, len(df))
            batch_df = df.iloc[i:batch_end]

            for idx, row in batch_df.iterrows():
                result = get_answer(row)
                results.append(result)

                # 统计成功/失败
                if result != "调用结果出错":
                    success_count += 1
                else:
                    error_count += 1

                # 更新进度条信息
                pbar.set_postfix({
                    '成功': success_count,
                    '失败': error_count,
                    '成功率': f"{success_count/(success_count+error_count)*100:.1f}%" if (success_count+error_count) > 0 else "0%"
                })

                pbar.update(1)

    df[target_column] = results
    print(f"\n翻译完成！总计: {len(df)} 条，成功: {success_count} 条，失败: {error_count} 条")
    return df

print("="*60)
print("方法4: 实时显示翻译内容和结果")

def translate_with_content_display(df, column_name='act', target_column='act_zh'):
    """实时显示翻译内容和结果"""
    results = []

    with tqdm(total=len(df), desc="翻译进度", unit="条",
              bar_format='{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]') as pbar:

        for idx, row in df.iterrows():
            # 显示当前处理的内容
            current_text = str(row[column_name])[:40] + "..." if len(str(row[column_name])) > 40 else str(row[column_name])

            # 执行翻译
            result = get_answer(row)
            results.append(result)

            # 显示翻译结果
            if result != "调用结果出错":
                result_display = result[:30] + "..." if len(result) > 30 else result
                pbar.set_postfix_str(f"原文: {current_text} -> 译文: {result_display}")
            else:
                pbar.set_postfix_str(f"翻译失败: {current_text}")

            pbar.update(1)

    df[target_column] = results
    return df

# 使用说明
print("\n" + "="*60)
print("📋 使用说明:")
print("1. 确保已安装tqdm: !pip install tqdm")
print("2. 选择以下任一方法:")
print()
print("🚀 最简单（推荐）:")
print("   tqdm.pandas(desc='翻译进度')")
print("   df['act_zh'] = df.progress_apply(get_answer, axis=1)")
print()
print("🔧 手动控制:")
print("   df = translate_with_manual_progress(df)")
print()
print("📊 详细统计:")
print("   df = translate_with_detailed_progress(df)")
print()
print("👀 实时显示:")
print("   df = translate_with_content_display(df)")

# 实际使用的代码模板
usage_template = '''
# 🎯 直接复制到你的notebook中使用：

# 1. 安装tqdm（如果还没有）
!pip install tqdm

# 2. 导入tqdm
from tqdm import tqdm
import pandas as pd

# 3. 启用pandas的tqdm支持
tqdm.pandas(desc="翻译进度")

# 4. 使用progress_apply替代apply（只需要改这一行！）
df['act_zh'] = df.progress_apply(get_answer, axis=1)

# 就这么简单！你会看到一个漂亮的进度条显示翻译进度
'''

print("\n" + "="*60)
print("📝 使用模板:")
print(usage_template)
