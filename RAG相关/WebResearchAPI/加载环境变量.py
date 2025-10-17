import os
import subprocess

# 临时加载环境变量配置
def load_env_from_zshrc():
    result = subprocess.run(
        ['zsh', '-c', 'source ~/.zshrc && env'],
        capture_output=True, text=True
    )
    env_vars = {}
    for line in result.stdout.splitlines():
        if '=' in line:
            key, value = line.split('=', 1)
            env_vars[key] = value
    return env_vars

# 加载并使用环境变量
env_vars = load_env_from_zshrc()
api_key = env_vars.get("BOCHA_API_KEY")
print(api_key)