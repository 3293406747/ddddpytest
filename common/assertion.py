from common.logger import logger


class Assertion:
	""" 断言 """
	@classmethod
	def equal(cls,expect,actual,name=None):
		""" 相等断言 """
		if isinstance(expect,list|tuple|set) and isinstance(actual,list|tuple|set):
			for i in range(len(expect)):
				try:
					assert expect[i] == actual[i]
					msg = f"{name or ''}断言通过:{str(expect[i])}等于{str(actual[i])}"
					logger.success(msg)
				except AssertionError:
					msg = f"{name or ''}断言失败:{str(expect[i])}不等于{str(actual[i])}"
					logger.error(msg)
					raise AssertionError(msg) from None
		elif isinstance(expect,str|int|float) and isinstance(actual,str|int|float):
			try:
				assert expect == actual
				msg = f"{name or ''}断言通过:{str(expect)}等于{str(actual)}"
				logger.success(msg)
			except AssertionError:
				msg = f"{name or ''}断言失败:{str(expect)}不等于{str(actual)}"
				logger.error(msg)
				raise AssertionError(msg) from None

	@classmethod
	def unequal(cls,expect,actual,name=None):
		""" 不相等断言 """
		if isinstance(expect,list|tuple|set) and isinstance(actual,list|tuple|set):
			for i in range(len(expect)):
				try:
					assert expect[i] != actual[i]
					msg = f"{name or ''}断言通过:{str(expect[i])}不等于{str(actual[i])}"
					logger.success(msg)
				except AssertionError:
					msg = f"{name or ''}断言失败:{str(expect[i])}等于{str(actual[i])}"
					logger.error(msg)
					raise AssertionError(msg) from None
		elif isinstance(expect,str|int|float) and isinstance(actual,str|int|float):
			try:
				assert expect != actual
				msg = f"{name or ''}断言通过:{str(expect)}不等于{str(actual)}"
				logger.success(msg)
			except AssertionError:
				msg = f"{name or ''}断言失败:{str(expect)}等于{str(actual)}"
				logger.error(msg)
				raise AssertionError(msg) from None


	@classmethod
	def contian(cls,expect,actual,name=None):
		""" 包含断言 """
		if isinstance(expect,list|tuple|set):
			for i in expect:
				try:
					assert i in actual
					msg = f"{name or ''}断言通过:{str(i)}在{actual:20s}中存在"
					logger.success(msg)
				except AssertionError:
					msg = f"{name or ''}断言失败:{str(i)}在{actual:20s}中不存在"
					logger.error(msg)
					raise AssertionError(msg) from None
		elif isinstance(expect,str):
			try:
				assert expect in actual
				msg = f"{name or ''}断言通过:{expect}在{actual:20s}中存在"
				logger.success(msg)
			except AssertionError:
				msg = f"{name or ''}断言失败:{expect}在{actual:20s}中不存在"
				logger.error(msg)
				raise AssertionError(msg) from None

	@classmethod
	def uncontian(cls,expect,actual,name=None):
		""" 不包含断言 """
		if isinstance(expect,list|tuple|set):
			for i in expect:
				try:
					assert i not in actual
					msg = f"{name or ''}断言通过:{str(i)}在{actual:20s}中不存在"
					logger.success(msg)
				except AssertionError:
					msg = f"{name or ''}断言失败:{str(i)}在{actual:20s}中存在"
					logger.error(msg)
					raise AssertionError(msg) from None
		elif isinstance(expect,str):
			try:
				assert expect not in actual
				msg = f"{name or ''}断言通过:{expect}在{actual:20s}中不存在"
				logger.success(msg)
			except AssertionError:
				msg = f"{name or ''}断言失败:{expect}在{actual:20s}中存在"
				logger.error(msg)
				raise AssertionError(msg) from None
