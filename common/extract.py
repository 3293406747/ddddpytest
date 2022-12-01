import json
import re
import jsonpath


class Extract:
	""" 提取响应中的内容 """

	@staticmethod
	def json(data, pattern, index=None):
		""" json提取 """
		return Factory.create(method="json",data=data,pattern=pattern,index=index)

	@staticmethod
	def match(data,pattern,index=None):
		""" 正则提取 """
		return Factory.create(method="match", data=data, pattern=pattern, index=index)


class Factory:

	@classmethod
	def create(cls,method,data,pattern,index):
		# json提取
		if method == "json":
			result = Method.json(data=data,pattern=pattern)
		# 正则提取
		elif method == "match":
			result = Method.match(data=data,pattern=pattern)
		else:
			msg = "提取方式不支持。"
			raise Exception(msg)
		if not result:
			data = json.dumps(data, ensure_ascii=False) if isinstance(data,dict) else data
			raise Exception(f"要提取的值{pattern}在{data}中不存在")
		if index is not None:
			result = result[index]
		return result

class Method:

	@classmethod
	def json(cls,data,pattern):
		obj = json.loads(data) if isinstance(data, str) else data
		result = jsonpath.jsonpath(obj=obj, expr=pattern)
		return result

	@classmethod
	def match(cls,data,pattern):
		obj = json.dumps(data, ensure_ascii=False) if isinstance(data, dict) else data
		result = re.findall(pattern=pattern, string=obj)
		return result



extract = Extract()