from common.logger.logger import logger


class Method:

	@classmethod
	def equal_unqual(cls, method, expect, actual, name):
		# list|tuple|set
		if not isinstance(expect, (list, tuple, set)) or not isinstance(actual, (list, tuple, set)):
			msg = f"{expect}与{actual}类型不一致或类型格式不支持。"
			raise Exception(msg)
		for i in range(len(expect)):
			try:
				# 相等断言
				if method == "equal":
					assert expect[i] == actual[i]
					msg = f"{name or ''}断言通过:{str(expect[i])}等于{str(actual[i])}"
				# 不相等断言
				else:
					assert expect[i] != actual[i]
					msg = f"{name or ''}断言通过:{str(expect[i])}不等于{str(actual[i])}"
				logger.success(msg)
			except AssertionError:
				if method == "equal":
					msg = f"{name or ''}断言失败:{str(expect[i])}不等于{str(actual[i])}"
				else:
					msg = f"{name or ''}断言失败:{str(expect[i])}等于{str(actual[i])}"
				logger.error(msg)
				raise AssertionError(msg) from None

	@classmethod
	def contain_uncontain(cls, method, expect, actual, name):
		# list|tuple|set
		if not isinstance(expect, (list, tuple, set)):
			msg = f"{expect}类型格式不支持。"
			raise Exception(msg)
		for i in expect:
			try:
				# 包含断言
				if method == "contain":
					assert i in actual
					msg = f"{name or ''}断言通过:{str(i)}在{actual:.255s}中存在"
				# 不包含断言
				else:
					assert i not in actual
					msg = f"{name or ''}断言通过:{str(i)}在{actual:.255s}中不存在"
				logger.success(msg)
			except AssertionError:
				if method == "contain":
					msg = f"{name or ''}断言失败:{str(i)}在{actual:.255s}中不存在"
				else:
					msg = f"{name or ''}断言失败:{str(i)}在{actual:.255s}中存在"
				logger.error(msg)
				raise AssertionError(msg) from None