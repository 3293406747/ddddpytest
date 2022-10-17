import json
import re
from json import JSONDecodeError
import jsonpath
from common.logger import logger

class AssertionFactory:
	"""响应断言"""

	@classmethod
	def create(cls,target,response,pattern=None,expect=None,name=None,index=0):
		if pattern and not isinstance(pattern,str):
			raise TypeError('pattern must be a string')
		match str(target).lower():
			case 'responsejson':
				if expect:
					return ResponseJson(pattern, response, index).equal(expect,name)
				return ResponseJson(pattern, response, index).exist(name)
			case 'responsetext':
				try:
					response = json.dumps(response.json(), ensure_ascii=False)
				except JSONDecodeError:
					response.encoding = 'utf-8'
					response = response.text
				if expect:
					ResponseText(pattern, response, index).equal(expect,name)
				return ResponseText(pattern,response,index).exist(name)
			case 'responseheader':
				if expect:
					ResponseHeader(pattern, response).equal(expect,name)
				return ResponseHeader(pattern,response).exist(name)
			case 'status':
				return ResponseStatus(response).equal(expect,name)
			case _:
				raise ValueError


class ResponseJson:
	""" json方式断言 """
	__instance = None

	def __new__(cls, *args, **kwargs):
		if not cls.__instance:
			cls.__instance = object.__new__(cls)
		return cls.__instance

	def __init__(self, pattern, response, index):
		self.__index = index
		self.__pattern = pattern
		self.__values: list | bool = jsonpath.jsonpath(response.json(), pattern)

	def equal(self, expect,name):
		if not isinstance(expect, str | int | float):
			raise ValueError("预期值必须是字符串、整数或小数")
		if self.__values and expect == self.__values[self.__index]:
			msg = f"{name or ''}断言成功：{self.__pattern}等于{self.__values[self.__index]}"
			logger.success(msg)
		elif not self.__values:
			msg = f"{name or ''}断言失败：预期结果'{expect}'不等于实际结果'{self.__values}'"
			logger.error(msg)
			raise SystemExit(1)
		else:
			msg = f"{name or ''}断言失败：预期结果'{expect}'不等于实际结果'{self.__values[self.__index]}'"
			logger.error(msg)
			raise SystemExit(1)

	def exist(self,name):
		if self.__values:
			msg = f"{name or ''}断言成功：{self.__pattern}存在，值为{self.__values[self.__index]}"
			logger.success(msg)
		else:
			msg = f"{name or ''}断言失败：{self.__pattern}不存在"
			logger.error(msg)
			raise SystemExit(1)


class ResponseText:
	""" 正则表达式方式断言 """
	__instance = None

	def __new__(cls, *args, **kwargs):
		if not cls.__instance:
			cls.__instance = object.__new__(cls)
		return cls.__instance

	def __init__(self, pattern, response, index):
		self.__pattern = pattern
		self.__index = index
		self.__values: list = re.findall(self.__pattern, response)

	def equal(self, expect,name):
		if not isinstance(expect, str | int | float):
			raise ValueError("预期值必须是字符串、整数或小数")
		if self.__values and expect == self.__values[self.__index]:
			msg = f"{name or ''}断言成功：{self.__pattern}等于{self.__values[self.__index]}"
			logger.success(msg)
		elif not self.__values:
			msg = f"{name or ''}断言失败：预期结果'{expect}'不等于实际结果'{self.__values}'"
			logger.error(msg)
			raise SystemExit(1)
		else:
			msg = f"{name or ''}断言失败：预期结果'{expect}'不等于实际结果'{self.__values[self.__index]}'"
			logger.error(msg)
			raise SystemExit(1)

	def exist(self,name):
		if self.__values:
			msg = f"{name or ''}断言成功：{self.__pattern}存在，值为{self.__values[self.__index]}"
			logger.success(msg)
		else:
			msg = f"{name or ''}断言失败：{self.__pattern}不存在"
			logger.error(msg)
			raise SystemExit(1)


class ResponseHeader:
	""" 响应头断言 """
	__instance = None

	def __new__(cls, *args, **kwargs):
		if not cls.__instance:
			cls.__instance = object.__new__(cls)
		return cls.__instance

	def __init__(self,pattern,response):
		self.__pattern = pattern
		self.__value = response.headers.get(pattern)

	def equal(self,expect,name):
		if not isinstance(expect, str | int | float):
			raise ValueError("预期值必须是字符串、整数或小数")
		if self.__value == expect:
			msg = f"{name or ''}断言成功：'{self.__pattern}'等于'{expect}'"
			logger.success(msg)
		else:
			msg = f"{name or ''}断言失败：预期值'{expect}'不等于实际值'{self.__value}'"
			logger.error(msg)
			raise SystemExit(1)

	def exist(self,name):
		if self.__value:
			msg = f"{name or ''}断言成功：{self.__pattern}存在，值为{self.__value}"
			logger.success(msg)
		else:
			msg = f"{name or ''}断言失败：{self.__pattern}不存在"
			logger.error(msg)
			raise SystemExit(1)


class ResponseStatus:
	""" 响应状态断言 """
	__instance = None

	def __new__(cls, *args, **kwargs):
		if not cls.__instance:
			cls.__instance = object.__new__(cls)
		return cls.__instance

	def __init__(self,response):
		self.__value = response.status_code

	def equal(self,expect,name):
		if not isinstance(expect, int):
			raise ValueError("预期值必须是整数")
		if self.__value == expect:
			msg = f"{name or ''}断言成功：状态码等于{self.__value}"
			logger.success(msg)
		else:
			msg = f"{name or ''}断言失败：预期值'{expect}'不等于实际值'{self.__value}'"
			logger.error(msg)
			raise SystemExit(1)