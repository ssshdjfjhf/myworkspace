import os

def set_unix_env_permanent(env_name, env_value):
    """
    macOS/Linux永久设置环境变量（写入用户级shell配置文件）
    :param env_name: 环境变量名
    :param env_value: 环境变量值
    """
    # 1. 确定当前shell类型（zsh或bash），找到对应的配置文件路径
    current_shell = os.environ.get("SHELL", "")
    if "zsh" in current_shell:
        config_path = os.path.expanduser("~/.zshrc")  # macOS默认zsh配置文件
    elif "bash" in current_shell:
        config_path = os.path.expanduser("~/.bashrc")  # Linux默认bash配置文件
    else:
        raise ValueError(f"未识别的shell类型：{current_shell}，请手动指定配置文件路径")

    # 2. 构造环境变量的配置语句（避免重复写入）
    env_line = f'export {env_name}="{env_value}"'  # 标准的shell环境变量配置格式

    # 3. 检查配置文件中是否已存在该环境变量，避免重复添加
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            content = f.read()
        if env_line in content:
            print(f"环境变量 {env_name} 已存在于 {config_path}，无需重复设置")
            return
    except FileNotFoundError:
        # 若配置文件不存在（如手动删除），则创建新文件
        pass

    # 4. 追加环境变量到配置文件
    with open(config_path, "a", encoding="utf-8") as f:
        f.write(f"\n{env_line}\n")  # 换行分隔，避免和其他内容混淆

    print(f"macOS/Linux环境变量 {env_name} 已写入 {config_path}")
    print("提示：需执行 source ~/.zshrc（或.bashrc） 或重启终端，环境变量才会生效")

if __name__ == "__main__":
    # 调用函数：设置AppId环境变量
    set_unix_env_permanent(
        env_name="BOCHA_API_KEY",
        env_value="sk-95e8f0f28c414438856130a44676778e"  # 替换为真实AppId
    )
