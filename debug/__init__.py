from functools import partial

from common.request.automatic import auto_request
from utils.logger import loggerx
from utils.variables_manager import SystemVariablesManager, FileVariablesManager

# 日志记录器配置
LOG_CONFIG_PATH = "debug/config/local.yaml"

# 日志记录器
loggerx.filename = LOG_CONFIG_PATH
loggerx.logger.debug("日志启动成功\n")

# 系统变量
system_variables = SystemVariablesManager()
# 文件变量
File_Variables_CONFIG_PATH = "debug/environment/local.yaml"
file_variables = FileVariablesManager(File_Variables_CONFIG_PATH)

# 合并变量
merged_variables = {**system_variables.pool, **file_variables.pool}

# 构造偏函数
auto_request = partial(auto_request, variables_pool=merged_variables, logger=loggerx.logger)