import re,importlib


class Type:

	factory = importlib.import_module("common.case.factory")
	parse = importlib.import_module("common.case.parse")

	@classmethod
	def vary(cls, key, value, mapping, obj):
		""" 使用变量 """
		if isinstance(value, str):
			res = re.match(r"^\$\{(.*?)\}$", value)
			if res and mapping.get(res.group(1)):
				obj[key] = mapping.get(res.group(1))
		elif isinstance(value, (list, dict)):
			Factory = getattr(cls.factory,"Factory")
			obj[key] = Factory.create(method="vary", obj=value, mapping=mapping)

	@classmethod
	def func(cls, key, value, obj):
		""" 调用python函数 """
		if isinstance(value, str):
			res = re.match(r"^\{\{(.*?)\}\}$", value)
			if res:
				parse = getattr(cls.parse, "parse")
				obj[key] = parse(res)
		elif isinstance(value, (list, dict)):
			Factory = getattr(cls.factory, "Factory")
			obj[key] = Factory.create(method="func", obj=value)