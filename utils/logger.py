"""
logger日志
"""
import sys

from loguru import logger

from common.read.config import read_config


class Logger:
	""" 日志管理 """

	def __init__(self):
		self.logger = logger
		self._filename = ""
		self.logger.remove()

	@property
	def filename(self):
		return self._filename

	@filename.setter
	def filename(self, value):
		self._filename = value
		self._add()

	def _add(self):
		# 控制台日志
		self.logger.add(
			sink=sys.stderr,
			**read_config(self._filename)["logger"]["console"],
		)
		# 文件日志
		self.logger.add(
			**read_config(self._filename)["logger"]["file"],
		)
		# 文件错误日志
		self.logger.add(
			**read_config(self._filename)["logger"]["errorFile"],
		)


loggerx = Logger()
