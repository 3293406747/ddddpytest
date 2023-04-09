"""
断言
"""
from abc import abstractmethod
from functools import partial
import numbers

from utils.metaclass import SingletonABCMeta


class Mode(metaclass=SingletonABCMeta):
	""" 抽象基类，定义 execute 方法 """

	@abstractmethod
	def execute(self, expect, actual) -> None:
		pass

	@staticmethod
	def format_param(target) -> list:
		"""转换为列表"""
		if isinstance(target, (str, numbers.Number)):
			return [target]
		elif isinstance(target, (tuple, set)):
			return list(target)
		elif isinstance(target, list):
			return target
		else:
			msg = f"不支持的类型{type(target)}"
			raise TypeError(msg)


class Equal(Mode):
	"""相等模式"""

	def __init__(self, flag=False):
		self.flag = flag

	def execute(self, expect, actual):
		expect, actual = self.format_param(expect), self.format_param(actual)  # 转换为列表
		msg = self.check_len(expect, actual)  # 检查长度是否一致
		if msg:
			return msg
		assert_fn = partial(self.assert_not_equal if self.flag else self.assert_equal)
		for expect_item, actual_item in zip(expect, actual):  # 对于 list 进行逐个元素的断言
			msg = assert_fn(expect_item, actual_item)
			if msg:
				return msg
		msg = "断言通过"
		return msg

	@staticmethod
	def check_len(expect: list, actual: list):
		"""检查预期结果与实际结果长度是否相等"""
		if len(expect) != len(actual):
			msg = f"断言失败，预期结果列表长度{len(expect)}与实际结果列表长度{len(actual)}不一致"
			return msg

	@staticmethod
	def assert_equal(expect, actual):
		"""相等断言"""
		if expect != actual:
			msg = f"断言失败，{expect}不等于{actual}。"
			return msg

	@staticmethod
	def assert_not_equal(expect, actual):
		"""不相等断言"""
		if expect == actual:
			msg = f"断言失败，{expect}等于{actual}"
			return msg


class Contain(Mode):
	"""包含模式"""

	def __init__(self, flag=False):
		self.flag = flag

	def execute(self, expect, actual: str):
		if not isinstance(actual, str):
			raise TypeError(f"{actual}必须是字符串类型")
		expect = self.format_param(expect)  # 转换为列表
		assert_fn = partial(self.assert_not_contain if self.flag else self.assert_contain)
		for expect_item in expect:  # 对于 list 进行逐个元素的断言
			msg = assert_fn(expect_item, actual)
			if msg:
				return msg
		msg = "断言通过"
		return msg

	@staticmethod
	def assert_contain(expect, actual):
		"""包含断言"""
		if expect not in actual:
			msg = f"断言失败，{expect}在实际结果中不存在"
			return msg

	@staticmethod
	def assert_not_contain(expect, actual):
		"""不包含断言"""
		if expect in actual:
			msg = f"断言失败，{expect}在实际结果中存在"
			return msg


class AssertionStrategy:
	"""策略类，根据传入的 strategy 执行相应的策略"""

	def __init__(self, strategy: Mode):
		self.strategy = strategy

	def execute(self, expect, actual):
		return self.strategy.execute(expect, actual)


class AssertData:
	""" 断言 """

	def __init__(self):
		self.equal_strategy = AssertionStrategy(Equal())
		self.not_equal_strategy = AssertionStrategy(Equal(True))
		self.contain_strategy = AssertionStrategy(Contain())
		self.not_contain_strategy = AssertionStrategy(Contain(True))

	def equal(self, expect, actual):
		""" 相等断言 """
		# return AssertionFactory.create(method="equal").excute(expect=expect, actual=actual, name=name)
		return self.equal_strategy.execute(expect=expect, actual=actual)

	def unequal(self, expect, actual):
		""" 不相等断言 """
		# return AssertionFactory.create(method="unequal").excute(expect=expect, actual=actual, name=name)
		return self.not_equal_strategy.execute(expect=expect, actual=actual)

	def contian(self, expect, actual):
		""" 包含断言 """
		# return AssertionFactory.create(method="contain").excute(expect=expect, actual=actual, name=name)
		return self.contain_strategy.execute(expect=expect, actual=actual)

	def uncontian(self, expect, actual):
		""" 不包含断言 """
		# return AssertionFactory.create(method="uncontain").excute(expect=expect, actual=actual, name=name)
		return self.not_contain_strategy.execute(expect=expect, actual=actual)


assert_data = AssertData()

# class AssertionFactory:
# 	"""工厂类，根据传入的 method 创建相应的对象"""
#
# 	methods = {
# 		"equal": {"cls": Equal, "flag": False},
# 		"unequal": {"cls": Equal, "flag": True},
# 		"contain": {"cls": Contain, "flag": False},
# 		"uncontain": {"cls": Contain, "flag": True},
# 	}
#
# 	@classmethod
# 	@lru_cache(maxsize=None)
# 	def create(cls, method) -> Mode:
# 		if method not in cls.methods:
# 			msg = "不支持该类型的断言"
# 			raise ValueError(msg)
# 		config = cls.methods[method]
# 		return config["cls"](config["flag"])
