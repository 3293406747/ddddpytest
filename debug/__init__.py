from functools import partial

from common.read.config import read_config
from common.request.automatic import auto_request
from utils.logger_manager import Logger
from utils.variables_manager import SystemVariablesManager, FileVariablesManager

# 日志记录器配置
_console_config = read_config("debug/config/local.yaml")["logger"]["console"]
_file_config = read_config("debug/config/local.yaml")["logger"]["file"]
_error_file_config = read_config("debug/config/local.yaml")["logger"]["errorFile"]

# 日志记录器
logger = Logger(_console_config, _file_config, _error_file_config).logger

logger.debug('日志启动成功')

# 系统变量
system_variables = SystemVariablesManager()
# 文件变量
file_variables = FileVariablesManager("debug/environment/local.yaml")

# 合并变量
merged_variables = {**system_variables.pool, **file_variables.pool}

# 构造偏函数
auto_request = partial(auto_request, variables_pool=merged_variables, logger=logger)
