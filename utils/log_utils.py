import logging

from utils import config

# 获取配置文件中的日志等级配置
log_level = config.get("log_level")
level = logging.INFO if log_level is None else eval(log_level)

log = logging.getLogger(__name__)

# 设置日志级别
log.setLevel(level)
logging.getLogger('werkzeug').setLevel(logging.ERROR)
logging.getLogger('apscheduler').setLevel(logging.DEBUG)
# 创建文件处理器
file_handler = logging.FileHandler(config.get_root() + '/help_gf.log')
file_handler.setLevel(level)

# 创建控制台处理器
console_handler = logging.StreamHandler()
console_handler.setLevel(level)

# 创建格式化器
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# 将格式化器添加到处理器
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# 将处理器添加到日志对象
log.addHandler(file_handler)
log.addHandler(console_handler)
