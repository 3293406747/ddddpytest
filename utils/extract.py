"""
提取内容
"""
import json, re, jsonpath
from abc import ABCMeta,abstractmethod

class Mode(metaclass=ABCMeta):

	@abstractmethod
	def extract(self,data,pattern):
		pass

	def execute(self,data,pattern,index):
		result = self.extract(data,pattern)
		if not result:
			data = json.dumps(data, ensure_ascii=False) if isinstance(data, dict) else data
			raise Exception(f"要提取的值{pattern}在{data}中不存在")
		if index is not None:
			result = result[index]
		return result


class Json(Mode):
	""" json提取 """
	def extract(self,data,pattern):
		obj = json.loads(data) if isinstance(data, str) else data
		return jsonpath.jsonpath(obj=obj, expr=pattern)

class Match(Mode):
	""" 正则提取 """
	def extract(self,data,pattern):
		obj = json.dumps(data, ensure_ascii=False) if isinstance(data, dict) else data
		return re.findall(pattern=pattern, string=obj)

json_ = Json()
match_ = Match()


class Extract:
	""" 提取内容 """

	@staticmethod
	def json(data, pattern, index=None):
		""" json提取 """
		return json_.execute(data=data, pattern=pattern, index=index)

	@staticmethod
	def match(data, pattern, index=None):
		""" 正则提取 """
		return match_.execute(data=data, pattern=pattern, index=index)


extract = Extract()

