import sys
from loguru import logger
from common.yaml import read_config


logger_text = read_config()["logger"]

logger.remove()

# 控制台日志
logger.add(
	sink=sys.stderr,
	level=logger_text["level"],
	format=logger_text["format"],
	backtrace=True,
	diagnose=False
)

# 文件日志
logger.add(
	sink=logger_text["sink"],
	level=logger_text["level"],
	format=logger_text["format"],
	rotation = logger_text["rotation"],
	backtrace=True,
	diagnose=False
)

# logger.info("logger启动成功")