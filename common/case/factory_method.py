import json, re

from common.case.parse import parse


class Factory:

	@classmethod
	def create(cls, method, obj, mapping=None):
		if isinstance(obj, str):
			obj = json.loads(obj)
		if isinstance(obj, list):
			for key, value in enumerate(obj):
				if method == "vary":
					Method.vary(key=key, value=value, mapping=mapping, obj=obj)
				elif method == "func":
					Method.func(key=key, value=value, obj=obj)
				else:
					msg = "method not found"
					raise Exception(msg)
		elif isinstance(obj, dict):
			for key, value in obj.items():
				if method == "vary":
					Method.vary(key=key, value=value, mapping=mapping, obj=obj)
				elif method == "func":
					Method.func(key=key, value=value, obj=obj)
				else:
					msg = "method not found"
					raise Exception(msg)
		return obj


class Method:

	@classmethod
	def vary(cls, key, value, mapping, obj):
		""" 使用变量 """
		if isinstance(value, str):
			res = re.match(r"^\$\{(.*?)\}$", value)
			if res and mapping.get(res.group(1)):
				obj[key] = mapping.get(res.group(1))
		elif isinstance(value, (list, dict)):
			obj[key] = Factory.create(method="vary", obj=value, mapping=mapping)

	@classmethod
	def func(cls, key, value, obj):
		""" 调用python函数 """
		if isinstance(value, str):
			res = re.match(r"^\{\{(.*?)\}\}$", value)
			if res:
				obj[key] = parse(res)
		elif isinstance(value, (list, dict)):
			obj[key] = Factory.create(method="func", obj=value)
