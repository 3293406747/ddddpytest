from common.assertion.factory import Factory


class Assertion:
	""" 断言 """

	@classmethod
	def equal(cls, expect, actual, name=None):
		""" 相等断言 """
		return Factory.create(method="equal", expect=expect, actual=actual, name=name)

	@classmethod
	def unequal(cls, expect, actual, name=None):
		""" 不相等断言 """
		return Factory.create(method="unequal", expect=expect, actual=actual, name=name)

	@classmethod
	def contian(cls, expect, actual, name=None):
		""" 包含断言 """
		return Factory.create(method="contain", expect=expect, actual=actual, name=name)

	@classmethod
	def uncontian(cls, expect, actual, name=None):
		""" 不包含断言 """
		return Factory.create(method="uncontain", expect=expect, actual=actual, name=name)






