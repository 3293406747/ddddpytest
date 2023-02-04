import importlib
import json,re
from string import Template
from typing import Pattern
from functools import partial
from utils.variables import Variables
from common.variable.environments import Environments
from common.variable.globals import Globals
from abc import abstractmethod,ABCMeta

pattern: Pattern = re.compile(r"\{\{(.*?)\}\}")


def renderTemplate(data):
	""" 渲染模板 """
	data = json.dumps(data, ensure_ascii=False)
	# 使用变量
	merge = {**Variables().pool, **Globals().pool, **Environments().pool}
	# merge = Variables().pool | Globals().pool | Environments().pool
	genData = partial(Render.excute,mapping=merge)		# 构造偏函数
	data = genData(method="vary",obj=data)
	data = Template(json.dumps(data,ensure_ascii=False)).safe_substitute(merge)
	# 调用python函数
	data = genData(method="func", obj=data)
	data = pattern.sub(repl=parse, string=json.dumps(data,ensure_ascii=False))
	return json.loads(data)

def parse(reMatch):
	""" repl解析 """
	obj = importlib.import_module("utils.function")
	# obj = __import__("utils.function",fromlist=True)
	data = re.findall(r"\.?(.+?)\((.*?)\)", reMatch.group(1))
	for i in data:
		name, args = i[0], i[1]
		obj = args and getattr(obj, name)(*args.split(",")) or getattr(obj, name)()
	return obj


class Mode(metaclass=ABCMeta):

	@abstractmethod
	def excute(self,*args,**kwargs):
		pass


class UseFunction(Mode):
	""" 调用python函数 """
	def excute(self,key, value, obj):
		if isinstance(value, str):
			res = re.match(r"^\{\{(.*?)\}\}$", value)
			if res:
				obj[key] = parse(res)
		elif isinstance(value, (list, dict)):
			obj[key] = Render().excute(method="func", obj=value)

class UseVariables(Mode):
	""" 使用变量 """
	def excute(self,key, value, obj,mapping):
		if isinstance(value, str):
			res = re.match(r"^\$\{(.*?)\}$", value)
			if res and mapping.get(res.group(1)):
				obj[key] = mapping.get(res.group(1))
		elif isinstance(value, (list, dict)):
			obj[key] = Render().excute(method="vary", obj=value, mapping=mapping)

useFunction = UseFunction()
useVariables = UseVariables()

class Render:

	@classmethod
	def excute(cls, method, obj, mapping=None):
		if isinstance(obj, str):
			obj = json.loads(obj)
		if isinstance(obj, list):
			for key, value in enumerate(obj):
				if method == "vary":
					useVariables.excute(key=key, value=value, mapping=mapping, obj=obj)
				elif method == "func":
					useFunction.excute(key=key, value=value, obj=obj)
				else:
					msg = "method not found"
					raise ValueError(msg)
		elif isinstance(obj, dict):
			for key, value in obj.items():
				if method == "vary":
					useVariables.excute(key=key, value=value, mapping=mapping, obj=obj)
				elif method == "func":
					useFunction.excute(key=key, value=value, obj=obj)
				else:
					msg = "method not found"
					raise ValueError(msg)
		return obj