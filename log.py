import logging

import os


def get_project_dir():
    # 获取当前文件的绝对路径
    current_path = os.path.abspath(__file__)
    # 获取当前文件所在的目录
    current_dir = os.path.dirname(current_path)
    # 获取项目的根目录
    project_dir = os.path.dirname(current_dir)
    return project_dir


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logging.getLogger('apscheduler').setLevel(logging.DEBUG)
# 创建文件处理器
file_handler = logging.FileHandler(get_project_dir() + '/help_gf.log')
file_handler.setLevel(logging.DEBUG)

# 创建控制台处理器
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# 创建格式化器
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# 将格式化器添加到处理器
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# 将处理器添加到日志对象
logger.addHandler(file_handler)
logger.addHandler(console_handler)
