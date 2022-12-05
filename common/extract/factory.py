from common.extract.method import Method
import json


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