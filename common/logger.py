import sys
from loguru import logger as logging
from common.yaml_ import read_config


class Logger:
	"""项目日志管理"""
	def __init__(self):
		self.logger = logging
		self.logger.remove()
		# 控制台日志
		self.logger.add(
			sink=sys.stderr,
			**read_config()["logger"]["console"],
			backtrace=True,
			diagnose=False
		)
		# 文件日志
		self.logger.add(
			**read_config()["logger"]["file"],
			backtrace=True,
			diagnose=False
		)

logger = Logger().logger

logger.debug('日志启动成功')