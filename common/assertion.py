import json
from common.logger import logger


class Assertion:
	""" 断言 """
	@classmethod
	def equal(cls,expect,actual,name=None):
		""" 相等断言 """
		return Factory.create(method="equal",expect=expect,actual=actual,name=name)

	@classmethod
	def unequal(cls,expect,actual,name=None):
		""" 不相等断言 """
		return Factory.create(method="unequal",expect=expect,actual=actual,name=name)

	@classmethod
	def contian(cls,expect,actual,name=None):
		""" 包含断言 """
		return Factory.create(method="contain",expect=expect,actual=actual,name=name)

	@classmethod
	def uncontian(cls,expect,actual,name=None):
		""" 不包含断言 """
		return Factory.create(method="uncontain",expect=expect,actual=actual,name=name)


class Factory:

	@classmethod
	def create(cls,method,expect,actual,name=None):
		if method in ["equal","unequal"]:
			if isinstance(expect,(str, int, float)):
				expect = [expect]
			if isinstance(actual,(str, int, float)):
				actual = [actual]
			# list|tuple|set
			if isinstance(expect, (list, tuple, set)) and isinstance(actual, (list, tuple, set)):
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
			else:
				msg = f"{expect}与{actual}类型不一致或类型格式不支持。"
				raise Exception(msg)
		elif method in ["contain","uncontain"]:
			actual = json.dumps(actual, ensure_ascii=False) if isinstance(actual, dict) else actual
			# list|tuple|set
			if isinstance(expect,str):
				expect = [expect]
			if isinstance(expect, (list, tuple, set)):
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
			else:
				msg = f"{expect}类型格式不支持。"
				raise Exception(msg)
		else:
			msg = "断言格式不支持。"
			raise Exception(msg)