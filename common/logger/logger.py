import sys
from loguru import logger as logging
from common.read.read_config import read_config


class Logger:
	""" 日志管理 """
	def __init__(self):
		self.logger = logging
		self.logger.remove()
		# 控制台日志
		self.logger.add(
			sink=sys.stderr,
			**read_config()["logger"]["console"],
		)
	# 文件日志
		self.logger.add(
			**read_config()["logger"]["file"],
		)


logger = Logger().logger
logger.debug('日志启动成功')