import json
import re
from json import JSONDecodeError
import jsonpath


class Response:
	""" 响应 """
	def __init__(self,res):
		self.res = res

	@property
	def response(self):
		""" 响应 """
		return self.res

	def json(self):
		""" json格式数据 """
		return self.res.json()

	@property
	def text(self):
		""" 文本格式数据 """
		return self.res.text

	@property
	def enconding(self):
		""" 获取响应编码格式 """
		return self.res.encoding

	@enconding.setter
	def encoding(self,item):
		""" 设置响应编码格式 """
		self.res.encoding = item

	def content(self):
		return self.res.content

	@property
	def status_code(self):
		""" 响应状态码 """
		return self.res.status_code

	@property
	def headers(self):
		""" 响应头 """
		return self.res.headers

	def extractVariable(self):
		""" 提取响应中的内容 """
		return ExtractVariable(self.res)

class ExtractVariable:
	""" 提取响应中的内容 """
	def __init__(self,response):
		self.res = response

	def json(self,expr,index=None):
		""" json提取 """
		if index is None:
			extract = jsonpath.jsonpath(obj=self.res.json(), expr=expr)
		else:
			extract = jsonpath.jsonpath(obj=self.res.json(), expr=expr)[index]
		return extract

	def match(self,pattern,index=None):
		""" 正则提取 """
		try:
			data = json.dumps(self.res.json(), ensure_ascii=False)
		except JSONDecodeError:
			data = self.res.text
		if index is None:
			extract = re.findall(pattern=pattern, string=data)
		else:
			extract = re.findall(pattern=pattern, string=data)[index]
		return extract