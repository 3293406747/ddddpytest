import sys
from loguru import logger as logging
from common.yaml_ import read_config


class Logger:

	def __init__(self):
		self.logger = logging
		self.logger.remove()
		# 控制台日志
		self.logger.add(
			sink=sys.stderr,
			level=read_config()["logger"]["level"],
			format=read_config()["logger"]["format"],
			backtrace=True,
			diagnose=False
		)
		# 文件日志
		self.logger.add(
			**read_config()["logger"],
			backtrace=True,
			diagnose=False
		)

logger = Logger().logger