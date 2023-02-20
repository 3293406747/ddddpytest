"""
断言
"""
import json
from abc import ABCMeta, abstractmethod
from functools import lru_cache
from utils.logger import logger
import numbers


class Assertion:
	""" 断言 """

	@classmethod
	def equal(cls, expect, actual, name=None):
		""" 相等断言 """
		return AssertionFactory.create(method="equal").excute(expect=expect, actual=actual, name=name)

	@classmethod
	def unequal(cls, expect, actual, name=None):
		""" 不相等断言 """
		return AssertionFactory.create(method="unequal").excute(expect=expect, actual=actual, name=name)

	@classmethod
	def contian(cls, expect, actual, name=None):
		""" 包含断言 """
		return AssertionFactory.create(method="contain").excute(expect=expect, actual=actual, name=name)

	@classmethod
	def uncontian(cls, expect, actual, name=None):
		""" 不包含断言 """
		return AssertionFactory.create(method="uncontain").excute(expect=expect, actual=actual, name=name)


class Mode(metaclass=ABCMeta):
	""" 抽象基类，定义 execute 方法 """

	@abstractmethod
	def excute(self, expect, actual, name) -> None:
		pass


class Equal(Mode):
	"""相等模式"""

	def __init__(self, flag=False):
		self.flag = flag

	def excute(self, expect, actual, name) -> None:
		expect, actual = self.format_param(expect), self.format_param(actual)  # 转换为列表
		self.check_len(expect, actual)  # 检查长度是否一致
		for expect_item, actual_item in zip(expect, actual):  # 对于 list 进行逐个元素的断言
			if not self.flag:
				self.assert_equal(expect_item, actual_item, name)  # 相等断言
			else:
				self.assert_not_equal(expect_item, actual_item, name)  # 不相等断言

	@staticmethod
	def format_param(target) -> list:
		"""转换为列表"""
		# tuple|set
		if isinstance(target, (str, numbers.Number)):
			return [target]
		elif isinstance(target, (tuple, set)):
			return list(target)
		elif isinstance(target, list):
			return target
		else:
			msg = f"不支持的类型{type(target)}"
			raise TypeError(msg)

	@staticmethod
	def check_len(expect: list, actual: list) -> None:
		"""检查预期结果与实际结果长度是否相等"""
		if len(expect) != len(actual):
			msg = f"预期结果列表长度{len(expect)}与实际结果列表长度{len(actual)}不一致"
			raise AssertionError(msg)

	@staticmethod
	def assert_equal(expect, actual, name=None) -> None:
		"""相等断言"""
		try:
			assert expect == actual
			msg = f"{name or ''}断言通过:{expect}等于{actual}"
			logger.success(msg)
		except AssertionError:
			msg = f"{name or ''}断言失败:{expect}不等于{actual}"
			logger.error(msg)
			raise AssertionError(msg) from None

	@staticmethod
	def assert_not_equal(expect, actual, name=None) -> None:
		"""不相等断言"""
		try:
			assert expect != actual
			msg = f"{name or ''}断言通过:{expect}不等于{actual}"
			logger.success(msg)
		except AssertionError:
			msg = f"{name or ''}断言失败:{expect}等于{actual}"
			logger.error(msg)
			raise AssertionError(msg) from None


class Contain(Mode):
	"""包含模式"""

	def __init__(self, flag=False):
		self.flag = flag

	def excute(self, expect, actual, name) -> None:
		actual = self.format_actual(actual)  # 转换为json格式
		expect = self.format_expect(expect)  # 转换为列表
		for i in expect:  # 对于 list 进行逐个元素的断言
			if not self.flag:
				self.assert_contain(i, actual, name)  # 包含断言
			else:
				self.assert_not_contain(i, actual, name)  # 不包含断言

	@staticmethod
	def format_actual(target):
		"""转换为json格式"""
		if isinstance(target, dict):
			return json.dumps(target, ensure_ascii=False)
		return target

	@staticmethod
	def format_expect(target) -> list:
		"""转换为列表"""
		if isinstance(target, str):
			return [target]
		elif isinstance(target, (tuple, set)):
			return list(target)
		elif isinstance(target, list):
			return target
		else:
			msg = f"不支持的类型{type(target)}"
			raise TypeError(msg)

	@staticmethod
	def assert_contain(expect, actual, name=None) -> None:
		"""包含断言"""
		try:
			assert expect in actual
			msg = f"{name or ''}断言通过:{expect}在{actual:.255s}中存在"
			logger.success(msg)
		except AssertionError:
			msg = f"{name or ''}断言失败:{expect}在{actual:.255s}中不存在"
			logger.error(msg)
			raise AssertionError(msg) from None

	@staticmethod
	def assert_not_contain(expect, actual, name=None) -> None:
		"""不包含断言"""
		try:
			assert expect not in actual
			msg = f"{name or ''}断言通过:{expect}在{actual:.255s}中不存在"
			logger.success(msg)
		except AssertionError:
			msg = f"{name or ''}断言失败:{expect}在{actual:.255s}中存在"
			logger.error(msg)
			raise AssertionError(msg) from None


class AssertionFactory:
	"""工厂类，根据传入的 method 创建相应的对象"""

	methods = {
		"equal": {"cls": Equal, "flag": False},
		"unequal": {"cls": Equal, "flag": True},
		"contain": {"cls": Contain, "flag": False},
		"uncontain": {"cls": Contain, "flag": True},
	}

	@classmethod
	@lru_cache(maxsize=None)
	def create(cls, method) -> Mode:
		if method not in cls.methods:
			msg = "不支持该类型的断言"
			raise ValueError(msg)
		config = cls.methods[method]
		return config["cls"](config["flag"])


if __name__ == '__main__':
	Assertion.equal("test","test")
	Assertion.equal(1,1)
	Assertion.equal(["test"],["test"])
	Assertion.equal(("test",),("test",))
	Assertion.equal({"test"},{"test"})

	Assertion.unequal("test","text")
	Assertion.unequal(1,2)
	Assertion.unequal(["test"],["text"])
	Assertion.unequal(("test",),("text",))
	Assertion.unequal({"test"},{"text"})

	Assertion.contian("test","my test")
	Assertion.contian(["test"],"my test")
	Assertion.contian(("test",),"my test")
	Assertion.contian({"test"},"my test")

	Assertion.uncontian("text","my test")
	Assertion.uncontian(["text"],"my test")
	Assertion.uncontian(("text",),"my test")
	Assertion.uncontian({"text"},"my test")
