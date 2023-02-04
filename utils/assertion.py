"""
断言
"""
import json
from abc import ABCMeta,abstractmethod
from utils.logger import logger


class Assertion:
	""" 断言 """

	@classmethod
	def equal(cls, expect, actual, name=None):
		""" 相等断言 """
		return Factory.create(method="equal").excute(expect=expect, actual=actual, name=name)

	@classmethod
	def unequal(cls, expect, actual, name=None):
		""" 不相等断言 """
		return Factory.create(method="unequal").excute(expect=expect, actual=actual, name=name)

	@classmethod
	def contian(cls, expect, actual, name=None):
		""" 包含断言 """
		return Factory.create(method="contain").excute(expect=expect, actual=actual, name=name)

	@classmethod
	def uncontian(cls, expect, actual, name=None):
		""" 不包含断言 """
		return Factory.create(method="uncontain").excute(expect=expect, actual=actual, name=name)


class Factory:

	@classmethod
	def create(cls, method):
		if method in ["equal", "unequal"]:
			return Equal() if method == "equal" else Equal(True)
		elif method in ["contain", "uncontain"]:
			return Contain() if method == "contain" else Contain(True)
		else:
			msg = "断言格式不支持。"
			raise TypeError(msg)

class Mode(metaclass=ABCMeta):
	@abstractmethod
	def excute(self,expect, actual, name):
		pass

class Equal(Mode):

	def __init__(self,flag=False):
		self.flag = flag

	def excute(self,expect, actual, name):
		list(map(lambda x: [x] if isinstance(x, (str, int, float)) else x, [expect, actual]))
		# list|tuple|set
		if not isinstance(expect, (list, tuple, set)) or not isinstance(actual, (list, tuple, set)):
			msg = f"{expect}与{actual}类型不一致或类型格式不支持。"
			raise Exception(msg)
		for i in range(len(expect)):
			try:
				# 相等断言
				if not self.flag:
					assert expect[i] == actual[i]
					msg = f"{name or ''}断言通过:{str(expect[i])}等于{str(actual[i])}"
				# 不相等断言
				else:
					assert expect[i] != actual[i]
					msg = f"{name or ''}断言通过:{str(expect[i])}不等于{str(actual[i])}"
				logger.success(msg)
			except AssertionError:
				if not self.flag:
					msg = f"{name or ''}断言失败:{str(expect[i])}不等于{str(actual[i])}"
				else:
					msg = f"{name or ''}断言失败:{str(expect[i])}等于{str(actual[i])}"
				logger.error(msg)
				raise AssertionError(msg) from None

class Contain(Mode):

	def __init__(self,flag=False):
		self.flag = flag

	def excute(self,expect, actual, name):
		actual = json.dumps(actual, ensure_ascii=False) if isinstance(actual, dict) else actual
		expect = [expect] if isinstance(expect, str) else expect
		# list|tuple|set
		if not isinstance(expect, (list, tuple, set)):
			msg = f"{expect}类型格式不支持。"
			raise Exception(msg)
		for i in expect:
			try:
				# 包含断言
				if not self.flag:
					assert i in actual
					msg = f"{name or ''}断言通过:{str(i)}在{actual:.255s}中存在"
				# 不包含断言
				else:
					assert i not in actual
					msg = f"{name or ''}断言通过:{str(i)}在{actual:.255s}中不存在"
				logger.success(msg)
			except AssertionError:
				if not self.flag:
					msg = f"{name or ''}断言失败:{str(i)}在{actual:.255s}中不存在"
				else:
					msg = f"{name or ''}断言失败:{str(i)}在{actual:.255s}中存在"
				logger.error(msg)
				raise AssertionError(msg) from None





