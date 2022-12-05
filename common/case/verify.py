import copy
import json


class Verify:
	""" 校验用例格式 """
	def __init__(self,case):
		self.case_new = copy.deepcopy(case)
		self.case_str = json.dumps(case,ensure_ascii=False)

	def args_must(self):
		# 必选参数校验
		for key in ["casename", "request"]:
			if not self.case_new.get(key):
				msg = f"{self.case_str:.255s}必须包含一级关键字casename,request"
				raise Exception(msg)
		self.case_new.pop("casename")

	def request(self):
		# request校验
		request = self.case_new.pop("request")
		for key in ["url", "method"]:
			if not request.get(key):
				msg = f"{self.case_str:.255s}的request关键字下必须包含二级关键字url,method"
				raise Exception(msg)
			else:
				request.pop(key)
		requestOtherKeys = ["params", "data", "json", "files", "headers"]
		for i in request.keys():
			if i not in requestOtherKeys:
				msg = f"{self.case_str:.255s}的request关键字下不能包含除{','.join(requestOtherKeys)}之外的关键字。"
				raise Exception(msg)

	def args_unmust(self):
		# 非必选参数校验
		otherKeys = ["data_path","data_sheet", "extract", "assertion", "session"]
		for i in self.case_new.keys():
			if i not in otherKeys:
				msg = f"{self.case_str:.255s}不能包含除casename,request,{','.join(otherKeys)}之外的一级关键字。"
				raise Exception(msg)

	def extract(self):
		# extract校验
		if self.case_new.get("extract"):
			extractKeys = ["request", "response"]
			if not isinstance(self.case_new.get("extract"), dict):
				msg = f"{self.case_str:.255s}的extract关键字下必须为字典格式。"
				raise Exception(msg)
			for key, value in self.case_new.get("extract").items():
				if key not in extractKeys:
					msg = f"{self.case_str:.255s}的extract关键字下不能包含除{','.join(extractKeys)}之外的关键字。"
					raise Exception(msg)
				if not isinstance(value, dict):
					msg = f"{self.case_str:.255s}的extract关键字下的{key}必须为字典格式。"
					raise Exception(msg)

	def session(self):
		# session校验
		if self.case_new.get("session") and not isinstance(self.case_new.get("session"), int):
			msg = f"{self.case_str:.255s}的session关键字下必须整数格式。"
			raise Exception(msg)

	def assertion(self):
		# assertion校验
		if self.case_new.get("assertion") and isinstance(self.case_new.get("assertion"), dict):
			assertionKeys = ["contain", "uncontain", "equal", "unequal"]
			for i in self.case_new.get("assertion").keys():
				if i not in assertionKeys:
					msg = f"{self.case_str:.255s}的assertion关键字下不能包含除{','.join(assertionKeys)}之外的关键字。"
					raise Exception(msg)
				elif i in ["equal", "unequal"]:
					for key in ["expect", "actual"]:
						if not isinstance(self.case_new["assertion"][i], list):
							msg = f"{self.case_str:.255s}的assertion关键字下的{i}必须是list格式。"
							raise Exception(msg)
						for j in self.case_new["assertion"][i]:
							if key not in j.keys():
								msg = f"{self.case_str:.255s}的assertion关键字下的{i}关键字下必须包含expect,actual关键字。"
								raise Exception(msg)
				elif i in ["contain", "uncontain"]:
					if not isinstance(self.case_new["assertion"][i], list):
						msg = f"{self.case_str:.255s}的assertion关键字下的{i}关键字必须为list格式。"
						raise Exception(msg)
		elif self.case_new.get("assertion") and not isinstance(self.case_new.get("assertion"), dict):
			msg = f"{self.case_str:.255s}的assertion关键字必须是字典格式。"
			raise Exception(msg)


def verify(case):
	""" 校验用例格式 """
	ver = Verify(case=case)
	ver.args_must()
	ver.request()
	ver.args_unmust()
	ver.extract()
	ver.session()
	ver.assertion()
	return case
