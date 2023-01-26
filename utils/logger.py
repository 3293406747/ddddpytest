"""
logger日志
"""
import sys,time
from loguru import logger as logging
from common.read.readConfig import readConfig


class Logger:
	""" 日志管理 """
	def __init__(self):
		self.logger = logging
		self.logger.remove()
		# 控制台日志
		self.logger.add(
			sink=sys.stderr,
			**readConfig()["logger"]["console"],
		)
		# 文件日志
		self.logger.add(
			sink = f'./logs/{time.strftime("%Y-%m-%d")}/log_{time.strftime("%H_%M_%S")}.log',
			**readConfig()["logger"]["file"],
		)
		# 文件错误日志
		self.logger.add(
			sink=f'./logs/{time.strftime("%Y-%m-%d")}/error.log',
			**readConfig()["logger"]["errorFile"],
		)


logger = Logger().logger
logger.debug('日志启动成功')