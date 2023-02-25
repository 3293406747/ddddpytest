import copy
from abc import abstractmethod, ABC

from utils.singleinstance import singleton


class CaseVerification(ABC):
	"""用例格式校验器"""

	def __init__(self):
		self._next_handler = None

	def set_next_handler(self, handler):
		self._next_handler = handler
		return handler

	@abstractmethod
	def verify_case(self, case):
		pass


@singleton
class VerifyMustKeys(CaseVerification):
	"""必选参数校验"""

	def verify_case(self, case):
		new_case = copy.deepcopy(case)
		for key in ["casename", "request"]:
			if not new_case.get(key):
				msg = f"用例必须包含一级关键字casename,request"
				raise Exception(msg)
		new_case.pop("casename")
		self._next_handler.verify_case(new_case)
		return case


@singleton
class VerifyRequestKeys(CaseVerification):
	"""请求参数校验"""

	def verify_case(self, case):
		request = case.pop("request")
		for key in ["url", "method"]:
			if not request.get(key):
				msg = f"用例的request关键字下必须包含二级关键字url,method"
				raise Exception(msg)
			else:
				request.pop(key)
		requestOtherKeys = ["params", "data", "json", "files", "headers"]
		for i in request.keys():
			if i not in requestOtherKeys:
				msg = f"用例的request关键字下不能包含除{','.join(requestOtherKeys)}之外的关键字。"
				raise Exception(msg)
		self._next_handler.verify_case(case)
		return case


@singleton
class VerifyNotMustKeys(CaseVerification):
	"""非必选参数校验"""

	def verify_case(self, case):
		otherKeys = ["data_path", "data_sheet", "extract", "assertion", "session"]
		for i in case.keys():
			if i not in otherKeys:
				msg = f"用例不能包含除casename,request,{','.join(otherKeys)}之外的一级关键字。"
				raise Exception(msg)
		self._next_handler.verify_case(case)
		return case


@singleton
class VerifyExtractKeys(CaseVerification):
	"""提取参数校验"""

	def verify_case(self, case):
		if case.get("extract"):
			extractKeys = ["request", "response"]
			if not isinstance(case.get("extract"), dict):
				msg = f"用例的extract关键字下必须为字典格式。"
				raise Exception(msg)
			for key, value in case.get("extract").items():
				if key not in extractKeys:
					msg = f"用例的extract关键字下不能包含除{','.join(extractKeys)}之外的关键字。"
					raise Exception(msg)
				if not isinstance(value, dict):
					msg = f"用例的extract关键字下的{key}必须为字典格式。"
					raise Exception(msg)
		self._next_handler.verify_case(case)
		return case


@singleton
class VerifySessionKeys(CaseVerification):
	"""session参数校验"""

	def verify_case(self, case):
		if case.get("session") and not isinstance(case.get("session"), int):
			msg = f"用例的session关键字下必须整数格式。"
			raise Exception(msg)
		self._next_handler.verify_case(case)
		return case


@singleton
class VerifyAssertionKeys(CaseVerification):
	"""断言参数校验"""

	def verify_case(self, case):
		if case.get("assertion") and isinstance(case.get("assertion"), dict):
			assertionKeys = ["contain", "uncontain", "equal", "unequal"]
			for i in case.get("assertion").keys():
				if i not in assertionKeys:
					msg = f"用例的assertion关键字下不能包含除{','.join(assertionKeys)}之外的关键字。"
					raise Exception(msg)
				elif i in ["equal", "unequal"]:
					for key in ["expect", "actual"]:
						if not isinstance(case["assertion"][i], list):
							msg = f"用例的assertion关键字下的{i}必须是list格式。"
							raise Exception(msg)
						for j in case["assertion"][i]:
							if key not in j.keys():
								msg = f"用例的assertion关键字下的{i}关键字下必须包含expect,actual关键字。"
								raise Exception(msg)
				elif i in ["contain", "uncontain"]:
					if not isinstance(case["assertion"][i], list):
						msg = f"用例的assertion关键字下的{i}关键字必须为list格式。"
						raise Exception(msg)
		elif case.get("assertion") and not isinstance(case.get("assertion"), dict):
			msg = f"用例的assertion关键字必须是字典格式。"
			raise Exception(msg)
		return case


def verificationCase(case):
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
