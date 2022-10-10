import json
import re
from json import JSONDecodeError
import jsonpath
from common.logger import logger

class AssertionFactory:
	"""响应断言"""
	__instance = None

	def __new__(cls, *args, **kwargs):
		if not cls.__instance:
			cls.__instance = object.__new__(cls)
		return cls.__instance

	def __init__(self,cls):
		self.cls = cls

	def create(self,pattern,response,index):
		if not isinstance(pattern,str):
			raise TypeError('pattern must be a string')
		match self.cls:
			case 'responseJson':
				return ResponseJson(pattern, response, index)
			case 'responseText':
				try:
					response = json.dumps(response.json(), ensure_ascii=False)
				except JSONDecodeError:
					response.encoding = 'utf-8'
					response = response.text
				return ResponseText(pattern,response,index)
			case 'responseHeader':
				return ResponseHeader(pattern,response)
			case 'responseStatus':
				return ResponseStatus(pattern,response)
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

	def equal(self, expect):
		if not isinstance(expect, str | int | float):
			raise ValueError("预期值必须是字符串、整数或小数")
		if self.__values and expect == self.__values[self.__index]:
			logger.success(f"{self.__pattern}等于{self.__values[self.__index]}")
		elif not self.__values:
			msg = f"断言失败：预期结果'{expect}'不等于实际结果'{self.__values}'"
			logger.error(msg)
			raise SystemExit(1)
		else:
			msg = f"断言失败：预期结果'{expect}'不等于实际结果'{self.__values[self.__index]}'"
			logger.error(msg)
			raise SystemExit(1)

	def unequal(self, expect):
		if not isinstance(expect, str | int | float):
			raise ValueError("预期值必须是字符串、整数或小数")
		if not self.__values or expect != self.__values[self.__index]:
			logger.success(f"'{self.__pattern}'不等于'{expect}'")
		else:
			msg = f"断言失败：预期'{expect}'等于实际'{self.__values[self.__index]}'"
			logger.error(msg)
			raise SystemExit(1)

	def exist(self):
		if self.__values:
			logger.success(f"{self.__pattern}存在，值为{self.__values[self.__index]}")
		else:
			msg = f"{self.__pattern}不存在"
			logger.error(msg)
			raise SystemExit(1)

	def unexist(self):
		if not self.__values:
			logger.success(f"{self.__pattern}不存在")
		else:
			msg = f"{self.__pattern}存在，值为{self.__values[self.__index]}"
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

	def equal(self, expect):
		if not isinstance(expect, str | int | float):
			raise ValueError("预期值必须是字符串、整数或小数")
		if self.__values and expect == self.__values[self.__index]:
			logger.success(f"{self.__pattern}等于{self.__values[self.__index]}")
		elif not self.__values:
			msg = f"断言失败：预期结果'{expect}'不等于实际结果'{self.__values}'"
			logger.error(msg)
			raise SystemExit(1)
		else:
			msg = f"断言失败：预期结果'{expect}'不等于实际结果'{self.__values[self.__index]}'"
			logger.error(msg)
			raise SystemExit(1)

	def unequal(self, expect):
		if not isinstance(expect, str | int | float):
			raise ValueError("预期值必须是字符串、整数或小数")
		if not self.__values or expect != self.__values[self.__index]:
			logger.success(f"'{self.__pattern}'不等于'{expect}'")
		else:
			msg = f"断言失败：预期'{expect}'等于实际'{self.__values[self.__index]}'"
			logger.error(msg)
			raise SystemExit(1)

	def exist(self):
		if self.__values:
			logger.success(f"{self.__pattern}存在，值为{self.__values[self.__index]}")
		else:
			msg = f"{self.__pattern}不存在"
			logger.error(msg)
			raise SystemExit(1)

	def unexist(self):
		if not self.__values:
			logger.success(f"{self.__pattern}不存在")
		else:
			msg = f"{self.__pattern}存在，值为{self.__values[self.__index]}"
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

	def equal(self,expect):
		if not isinstance(expect, str | int | float):
			raise ValueError("预期值必须是字符串、整数或小数")
		if self.__value == expect:
			logger.success(f"'{self.__pattern}'等于'{expect}'")
		else:
			logger.error(f"预期值'{expect}'不等于实际值'{self.__value}'")
			raise SystemExit(1)

	def unequal(self,expect):
		if not isinstance(expect, str | int | float):
			raise ValueError("预期值必须是字符串、整数或小数")
		if self.__value != expect:
			logger.success(f"'{self.__pattern}'不等于'{expect}'")
		else:
			logger.error(f"预期值'{expect}'等于实际值'{self.__value}'")
			raise SystemExit(1)

	def exist(self):
		if self.__value:
			logger.success(f"{self.__pattern}存在，值为{self.__value}")
		else:
			msg = f"{self.__pattern}不存在"
			logger.error(msg)
			raise SystemExit(1)

	def unexist(self):
		if not self.__value:
			logger.success(f"{self.__pattern}不存在")
		else:
			msg = f"{self.__pattern}存在，值为{self.__value}"
			logger.error(msg)
			raise SystemExit(1)

class ResponseStatus:
	""" 响应状态断言 """
	__instance = None

	def __new__(cls, *args, **kwargs):
		if not cls.__instance:
			cls.__instance = object.__new__(cls)
		return cls.__instance

	def __init__(self,pattern,response):
		self.pattern = pattern
		self.__value = response.status_code

	def equal(self,expect):
		if not isinstance(expect, int):
			raise ValueError("预期值必须是整数")
		if self.__value == expect:
			logger.success(f"{self.pattern}等于{self.__value}")
		else:
			logger.error(f"预期值'{expect}'不等于实际值'{self.__value}'")
			raise SystemExit(1)

	def unequal(self,expect):
		if not isinstance(expect, int):
			raise ValueError("预期值必须是整数")
		if self.__value != expect:
			logger.success(f"{self.pattern}不等于{self.__value}")
		else:
			logger.error(f"预期值'{expect}'等于实际值'{self.__value}'")
			raise SystemExit(1)

	def exist(self):
		...

	def unexist(self):
		...