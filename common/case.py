import copy
import json
import re
from string import Template
from typing import Pattern
from common.variable import Variables, Globals, Environment
from common import function

pattern: Pattern = re.compile(r"\{\{(.*?)\}\}")
__all__ = ["renderTemplate"]


def renderTemplate(data):
	""" 渲染用例 """
	data = json.dumps(data, ensure_ascii=False)
	# 使用变量
	merge = {**Variables().pool, **Globals().pool, **Environment().pool}
	# merge = Variables().pool | Globals().pool | Environment().pool
	data = Template(data).safe_substitute(merge)
	# 调用python函数
	data = pattern.sub(repl=parse, string=data)
	return json.loads(data)


def verifyCase(case):
	""" 校验用例格式 """
	newCase: dict = copy.deepcopy(case)
	strcase = json.dumps(case, ensure_ascii=False)
	# 必选参数校验
	for key in ["casename", "request"]:
		if not newCase.get(key):
			msg = f"{strcase:.255s}必须包含一级关键字casename,request"
			raise Exception(msg)
	newCase.pop("casename")
	request = newCase.pop("request")
	# request校验
	for key in ["url", "method"]:
		if not request.get(key):
			msg = f"{strcase:.255s}的request关键字下必须包含二级关键字url,method"
			raise Exception(msg)
		else:
			request.pop(key)
	requestOtherKeys = ["params", "data", "json", "files"]
	for i in request.keys():
		if i not in requestOtherKeys:
			msg = f"{strcase:.255s}的request关键字下不能包含除url,method,params,data,json,files之外的关键字。"
			raise Exception(msg)
	# 非必选参数校验
	otherKeys = ["data_path", "extract", "assertion", "session"]
	for i in newCase.keys():
		if i not in otherKeys:
			msg = f"{strcase:.255s}不能包含除casename,request,data_path,extract,assertion,session之外的一级关键字。"
			raise Exception(msg)
	# extract校验
	if newCase.get("extract"):
		extractKeys = ["request", "response"]
		if not isinstance(newCase.get("extract"), dict):
			msg = f"{strcase:.255s}的extract关键字下必须为字典格式。"
			raise Exception(msg)
		for key, value in newCase.get("extract").items():
			if key not in extractKeys:
				msg = f"{strcase:.255s}的extract关键字下不能包含除{','.join(extractKeys)}之外的关键字。"
				raise Exception(msg)
			if not isinstance(value, dict):
				msg = f"{strcase:.255s}的extract关键字下的{key}必须为字典格式。"
				raise Exception(msg)
	# session校验
	if newCase.get("session") and not isinstance(newCase.get("session"), int):
		msg = f"{strcase:.255s}的session关键字下必须整数格式。"
		raise Exception(msg)
	# assertion校验
	if newCase.get("assertion") and isinstance(newCase.get("assertion"), dict):
		assertionKeys = ["contain", "uncontain", "equal", "unequal"]
		for i in newCase.get("assertion").keys():
			if i not in assertionKeys:
				msg = f"{strcase:.255s}的assertion关键字下不能包含除{','.join(assertionKeys)}之外的关键字。"
				raise Exception(msg)
			elif i in ["equal", "unequal"]:
				for key in ["expect", "actual"]:
					if not isinstance(newCase["assertion"][i], list):
						msg = f"{strcase:.255s}的assertion关键字下的{i}必须是list格式。"
						raise Exception(msg)
					for j in newCase["assertion"][i]:
						if key not in j.keys():
							msg = f"{strcase:.255s}的assertion关键字下的{i}关键字下必须包含expect,actual关键字。"
							raise Exception(msg)
			elif i in ["contain", "uncontain"]:
				if not isinstance(newCase["assertion"][i], list):
					msg = f"{strcase:.255s}的assertion关键字下的{i}关键字必须为list格式。"
					raise Exception(msg)
	elif newCase.get("assertion") and not isinstance(newCase.get("assertion"), dict):
		msg = f"{strcase:.255s}的assertion关键字必须是字典格式。"
		raise Exception(msg)
	return case


def parse(reMatch) -> str:
	""" repl解析 """
	obj = function
	data = re.findall(r"\.?(.+?)\((.*?)\)", reMatch.group(1))
	for i in data:
		name, args = i[0], i[1]
		if args:
			obj = getattr(obj, name)(*args.split(","))
		else:
			obj = getattr(obj, name)()
	if not isinstance(obj, str):
		msg = f"function {reMatch.group(1)} must return a string"
		raise TypeError(msg)
	return obj
