"""
logger日志
"""
import sys,time
from loguru import logger as logging
from common.read.readConfig import readConfig
from utils.singleinstance import singleton


@singleton
class Logger:
	""" 日志管理 """

	console_config = readConfig()["logger"]["console"]
	file_config = readConfig()["logger"]["file"]
	error_file_config = readConfig()["logger"]["errorFile"]

	def __init__(self):
		self.logger = logging
		self.logger.remove()
		# 控制台日志
		self.logger.add(
			sink=sys.stderr,
			**self.console_config,
		)
		# 文件日志
		self.logger.add(
			sink = f'./logs/{time.strftime("%Y-%m-%d")}/log_{time.strftime("%H_%M_%S")}.log',
			**self.file_config,
		)
		# 文件错误日志
		self.logger.add(
			sink=f'./logs/{time.strftime("%Y-%m-%d")}/error.log',
			**self.error_file_config,
		)


logger = Logger().logger
logger.debug('日志启动成功')