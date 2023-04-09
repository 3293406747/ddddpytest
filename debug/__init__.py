import sys
from functools import partial

from loguru import logger

from common.read.config import read_config
from common.request.automatic import auto_request
from utils.variables_manager import SystemVariablesManager, FileVariablesManager

# 日志记录器配置
LOG_CONFIG_PATH = "debug/config/local.yaml"
_console_config = read_config(LOG_CONFIG_PATH)["logger"]["console"]
_file_config = read_config(LOG_CONFIG_PATH)["logger"]["file"]
_error_file_config = read_config(LOG_CONFIG_PATH)["logger"]["errorFile"]

# 日志记录器
logger.remove()
logger.add(sink=sys.stderr, **_console_config)
logger.add(**_file_config)
logger.add(**_error_file_config)

logger.debug("日志启动成功\n")

# 系统变量
system_variables = SystemVariablesManager()
# 文件变量
File_Variables_CONFIG_PATH = "debug/environment/local.yaml"
file_variables = FileVariablesManager(File_Variables_CONFIG_PATH)

# 合并变量
merged_variables = {**system_variables.pool, **file_variables.pool}

# 构造偏函数
auto_request = partial(auto_request, variables_pool=merged_variables, logger=logger)