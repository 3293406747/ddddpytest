"""
提取内容
"""
import json, re, jsonpath
from abc import ABCMeta, abstractmethod
from functools import lru_cache


class Extract:
	""" 提取内容 """

	@staticmethod
	def json(data, pattern, index=None):
		""" json提取 """
		return ExtractFactory().create("json").execute(data=data, pattern=pattern, index=index)

	@staticmethod
	def match(data, pattern, index=None):
		""" 正则提取 """
		return ExtractFactory().create("match").execute(data=data, pattern=pattern, index=index)


class Mode(metaclass=ABCMeta):
	""" 抽象基类，定义 extract 方法和模板方法 """

	@abstractmethod
	def extract(self, data, pattern):
		pass

	def execute(self, data, pattern, index):
		data = json.dumps(data, ensure_ascii=False) if isinstance(data, dict) else data		# 转换为json格式
		result = self.extract(data, pattern)		# 提取
		if result is None:
			raise Exception(f"要提取的值{pattern}在{data}中不存在")
		if index is not None:
			result = result[index]
		return result


class Json(Mode):
	""" json提取 """

	def extract(self, data, pattern):
		try:
			obj = json.loads(data) if isinstance(data, str) else data
		except Exception:
			raise Exception(f"要提取的值{data}的数据格式不正确")
		return jsonpath.jsonpath(obj=obj, expr=pattern)


class Match(Mode):
	""" 正则提取 """

	def extract(self, data, pattern):
		return re.findall(pattern=pattern, string=data)


class ExtractFactory:
	"""工厂类，根据传入的 method 创建相应的对象"""

	methods = {
		"json": Json,
		"match": Match
	}

	@classmethod
	@lru_cache(maxsize=None)
	def create(cls, method) -> Mode:
		if method not in cls.methods:
			msg = f"不支持该类型的提取方式:{method}"
			raise ValueError(msg)
		return cls.methods[method]()


extract = Extract()
