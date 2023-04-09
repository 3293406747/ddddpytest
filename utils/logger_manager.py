"""
logger日志
"""
import sys

import loguru


class Logger:
	""" 日志管理 """

	def __init__(self,
				 console_config: dict | None = None,
				 file_config: dict | None = None,
				 error_file_config: dict | None = None
				 ) -> None:
		self.logger = loguru.logger
		self.logger.remove()
		# 控制台日志
		if console_config:
			self.logger.add(sink=sys.stderr, **console_config)
		# 文件日志
		if file_config:
			self.logger.add(**file_config)
		# 文件错误日志
		if error_file_config:
			self.logger.add(**error_file_config)
