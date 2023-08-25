# encoding:utf-8

import json
import os

config = {}


def init():
    pass


def get(key, default=None):
    if not key:
        return default
    if config.get(key):
        return config.get(key)
    return default


def load_config():
    global config
    config_path = f'{get_root()}/config.json'
    if not os.path.exists(config_path):
        raise Exception('配置文件不存在，请根据config-template.json模板创建config.json文件')

    config_str = read_file(config_path)
    # 将json字符串反序列化为dict类型
    config = json.loads(config_str)
    print("加载 配置 完成")
    return config


def get_current_path():
    return os.path.dirname(os.path.abspath(__file__))


# 获取项目根目录的路径
def get_root():
    current_path = get_current_path()
    project_dir = os.path.abspath(os.path.join(current_path, ".."))
    return project_dir


def read_file(path):
    with open(path, mode='r', encoding='utf-8') as f:
        return f.read()


load_config()

if __name__ == '__main__':
    print(config)
