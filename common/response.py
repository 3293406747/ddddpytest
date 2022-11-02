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

	@property
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