import json
import re
import jsonpath


class Extract:
	""" 提取响应中的内容 """

	@staticmethod
	def json(data,expr,index=None):
		""" json提取 """
		extract = jsonpath.jsonpath(obj=json.loads(data) if isinstance(data, str) else data, expr=expr)
		if not extract:
			raise Exception(f"要提取的值{expr}在{json.dumps(data, ensure_ascii=False)}中不存在")
		if index is not None:
			extract = extract[index]
		return extract

	@staticmethod
	def match(data,pattern,index=None):
		""" 正则提取 """
		res = json.dumps(data, ensure_ascii=False) if isinstance(data,dict) else data
		if index is None:
			extract = re.findall(pattern=pattern, string=res)
			if not extract:
				raise Exception(f"要提取的值{pattern}在{res}中不存在")
		else:
			extract = re.findall(pattern=pattern, string=res)
			if not extract:
				raise Exception(f"要提取的值{pattern}在{res}中不存在")
			extract = extract[index]
		return extract

extractVariable = Extract()