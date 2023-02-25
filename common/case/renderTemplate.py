import importlib
import json, re
from string import Template
from utils.variables import Variables
from common.variable.environments import Environments
from common.variable.globals import Globals


def renderTemplate(data) -> dict:
	""" 渲染模板 """
	# 合并变量池
	merge = {**Variables().pool, **Globals().pool, **Environments().pool}
	# merge = Variables().pool | Globals().pool | Environments().pool
	# jsonString = json.dumps(data, ensure_ascii=False)
	# data = RenderTemplate(VariablesStrategy()).excute(obj=jsonString, mapping=merge)
	# jsonString = json.dumps(data, ensure_ascii=False)
	# data = RenderTemplate(FunctionStrategy()).excute(obj=jsonString, mapping=merge)
	# 使用变量
	jsonString = json.dumps(data, ensure_ascii=False)
	data = Template(jsonString).safe_substitute(merge)
	# 调用python函数
	jsonString = json.dumps(data, ensure_ascii=False)
	data = re.sub(pattern=r"\{\{(.*?)\}\}", repl=parse, string=jsonString)
	# 返回字典格式数据
	dict_data = json.loads(data)
	return json.loads(dict_data) if isinstance(dict_data, str) else dict_data


utils_function = importlib.import_module("utils.function")
# utils_function = __import__("utils.function",fromlist=True)


def parse(target: re.Match):
	""" repl解析 """
	obj = utils_function
	data = re.findall(r"\.?(.+?)\((.*?)\)", target.group(1))
	for name, args in data:
		obj = args and getattr(obj, name)(*args.split(",")) or getattr(obj, name)()
	return obj


# from abc import ABC,abstractmethod

# class Strategy(ABC):
#
# 	@abstractmethod
# 	def excute(self,key, value, obj, mapping):
# 		pass
#
# class VariablesStrategy(Strategy):
# 	"""使用变量"""
# 	def __init__(self):
# 		self.renderTemplate = RenderTemplate(self)
#
# 	def excute(self,key, value, obj, mapping):
# 		if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
# 			if mapping.get(value[2:-1]):
# 				obj[key] = mapping.get(value[2:-1])
# 		elif isinstance(value, (list, dict)):
# 			obj[key] = self.renderTemplate.excute(obj=value, mapping=mapping)
#
# class FunctionStrategy(Strategy):
# 	"""调用python函数"""
# 	def __init__(self):
# 		self.renderTemplate = RenderTemplate(self)
#
# 	def excute(self,key, value, obj, mapping=None):
# 		if isinstance(value, str) and value.startswith("{{") and value.endswith("}}"):
# 			obj[key] = parse(re.match(pattern=r"^\{\{(.+?)\}\}$", string=value))
# 		elif isinstance(value, (list, dict)):
# 			obj[key] = self.renderTemplate.excute(obj=value)
#
#
# class RenderTemplate:
#
# 	def __init__(self,strategy:Strategy):
# 		self.strategy = strategy
#
# 	def excute(self, obj, mapping=None):
# 		if isinstance(obj, str):
# 			obj = json.loads(obj)
# 		if isinstance(obj, list):
# 			for key, value in enumerate(obj):
# 				self.strategy.excute(key=key, value=value, mapping=mapping, obj=obj)
# 		elif isinstance(obj, dict):
# 			for key, value in obj.items():
# 				self.strategy.excute(key=key, value=value, mapping=mapping, obj=obj)
# 		return obj