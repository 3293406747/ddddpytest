import copy
from abc import abstractmethod

from utils.metaclass import SingletonABCMeta


class CaseVerification(metaclass=SingletonABCMeta):
	"""用例格式校验器"""

	def __init__(self):
		self._next_handler = None

	def set_next_handler(self, handler):
		self._next_handler = handler
		return handler

	@abstractmethod
	def verify_case(self, case: dict) -> dict:
		pass


class VerifyMustKeys(CaseVerification):
	"""必选参数校验"""

	REQUIRED_KEYS = ("casename", "request")

	def verify_case(self, case: dict) -> dict:
		new_case = copy.deepcopy(case)
		for key in VerifyMustKeys.REQUIRED_KEYS:
			if key not in new_case:
				msg = f"用例必须包含一级关键字{key}"
				raise CaseVerificationError(msg)
		new_case.pop("casename")

		self._next_handler.verify_case(new_case)
		return case


class VerifyRequestKeys(CaseVerification):
	"""请求参数校验"""

	REQUIRED_KEYS = ("url", "method")
	ALLOWED_KEYS = ("params", "data", "json", "files", "headers")

	def verify_case(self, case: dict) -> dict:
		request = case.pop("request")
		for key in VerifyRequestKeys.REQUIRED_KEYS:
			if key not in request:
				msg = f"用例的request关键字下必须包含二级关键字{key}"
				raise CaseVerificationError(msg)
			else:
				request.pop(key)

		unexpected_keys = set(request) - set(VerifyRequestKeys.ALLOWED_KEYS)  # 集合时间复杂度比遍历时间复杂度低
		if unexpected_keys:
			msg = f"用例的request关键字下不能包含以下关键字：{', '.join(unexpected_keys)}"
			raise CaseVerificationError(msg)

		self._next_handler.verify_case(case)
		return case


class VerifyNotMustKeys(CaseVerification):
	"""非必选参数校验"""

	ALLOWED_KEYS = ("data_path", "data_sheet", "extract", "assertion", "session")

	def verify_case(self, case: dict) -> dict:
		unexpected_keys = set(case) - set(VerifyNotMustKeys.ALLOWED_KEYS)
		if unexpected_keys:
			msg = f"用例的一级关键字不能包含以下关键字：{', '.join(unexpected_keys)}"
			raise CaseVerificationError(msg)

		self._next_handler.verify_case(case)
		return case


class VerifyExtractKeys(CaseVerification):
	"""提取参数校验"""

	ALLOWED_KEYS = ("request", "response")

	def verify_case(self, case: dict) -> dict:
		extract = case.get("extract")
		if extract is None:
			return case

		if not isinstance(case.get("extract"), dict):
			msg = f"用例的extract关键字下必须为字典格式。"
			raise CaseVerificationError(msg)

		unexpected_keys = set(case.get("extract")) - set(VerifyExtractKeys.ALLOWED_KEYS)
		if unexpected_keys:
			msg = f"用例的extract关键字下不能包含以下关键字：{', '.join(unexpected_keys)}"
			raise CaseVerificationError(msg)

		for value in case.get("extract").values():
			if not isinstance(value, dict):
				msg = f"用例的extract关键字下的值{value}必须为字典格式。"
				raise CaseVerificationError(msg)

		self._next_handler.verify_case(case)
		return case


class VerifySessionKeys(CaseVerification):
	"""session参数校验"""

	def verify_case(self, case: dict) -> dict:
		if case.get("session") and not isinstance(case.get("session"), int):
			msg = f"用例的session关键字下必须整数格式。"
			raise CaseVerificationError(msg)

		self._next_handler.verify_case(case)
		return case


class VerifyAssertionKeys(CaseVerification):
	"""断言参数校验"""

	ALLOWED_KEYS = ("contain", "uncontain", "equal", "unequal")

	def verify_case(self, case: dict) -> dict:
		assertion = case.get("assertion")
		if assertion is None:
			return case

		if not isinstance(assertion, dict):
			msg = f"用例的assertion关键字必须是字典格式。"
			raise CaseVerificationError(msg)

		unexpected_keys = set(assertion) - set(VerifyAssertionKeys.ALLOWED_KEYS)
		if unexpected_keys:
			msg = f"用例的assertion关键字下不能包含以下关键字：{', '.join(unexpected_keys)}"
			raise CaseVerificationError(msg)

		for key, value in assertion.items():
			if not isinstance(value, list):
				msg = f"用例的assertion关键字下的{key}必须是list格式。"
				raise CaseVerificationError(msg)

			for item in value:
				if len(item) != 2:
					msg = f"用例的assertion关键字下的{key}关键字下必须包含2个元素。"
					raise CaseVerificationError(msg)

				if not all(k in item for k in ("expect", "actual")):
					msg = f"用例的assertion关键字下的{key}关键字下必须包含expect和actual关键字。"
					raise CaseVerificationError(msg)

		return case


class CaseVerificationError(Exception):
	pass


def verify_case(case):
	""" 校验用例格式 """
	handler1 = VerifyMustKeys()
	handler2 = VerifyRequestKeys()
	handler3 = VerifyNotMustKeys()
	handler4 = VerifyExtractKeys()
	handler5 = VerifySessionKeys()
	handler6 = VerifyAssertionKeys()
	handler1.set_next_handler(handler2).set_next_handler(handler3).set_next_handler(handler4).set_next_handler(
		handler5).set_next_handler(handler6)
	return handler1.verify_case(case)
