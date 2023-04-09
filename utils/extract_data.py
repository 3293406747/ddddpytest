"""
提取内容
"""
import json, re, jsonpath
from abc import abstractmethod

from utils.metaclass import SingletonABCMeta


class Mode(metaclass=SingletonABCMeta):
	""" 抽象基类，定义 extract 方法和模板方法 """

	@abstractmethod
	def extract(self, data, pattern):
		pass

	def templet_method(self, data, pattern, index):
		data = json.dumps(data, ensure_ascii=False) if isinstance(data, dict) else data  # 转换为json格式
		result = self.extract(data, pattern)  # 提取
		if result is None:
			raise ExtractError(f"要提取的值{pattern}在{data}中不存在")
		if index is not None:
			result = result[index]
		return result


class Json(Mode):
	""" json提取 """

	def extract(self, data, pattern):
		try:
			obj = json.loads(data) if isinstance(data, str) else data
		except Exception:
			raise ExtractError(f"要提取的值{data}的数据格式不正确")
		return jsonpath.jsonpath(obj=obj, expr=pattern)


class Match(Mode):
	""" 正则提取 """

	def extract(self, data, pattern):
		return re.findall(pattern=pattern, string=data)


class ExtractStrategy:
	"""策略类，根据传入的 strategy 执行相应的策略"""

	def __init__(self, strategy: Mode):
		self.strategy = strategy

	def execute(self, data, pattern, index):
		return self.strategy.templet_method(data, pattern, index)


class Extract:
	""" 提取内容 """

	json_extract_strategy = ExtractStrategy(Json())
	match_extract_strategy = ExtractStrategy(Match())

	@classmethod
	def json(cls, data, pattern, index=None):
		""" json提取 """
		# return ExtractFactory().create("json").templet_method(data=data, pattern=pattern, index=index)
		return cls.json_extract_strategy.execute(data, pattern, index)

	@classmethod
	def match(cls, data, pattern, index=None):
		""" 正则提取 """
		# return ExtractFactory().create("match").templet_method(data=data, pattern=pattern, index=index)
		return cls.match_extract_strategy.execute(data, pattern, index)


class ExtractError(Exception):
	pass

# class ExtractFactory:
# 	"""工厂类，根据传入的 method 创建相应的对象"""
#
# 	methods = {
# 		"json": Json,
# 		"match": Match
# 	}
#
# 	@classmethod
# 	@lru_cache(maxsize=None)
# 	def create(cls, method) -> Mode:
# 		if method not in cls.methods:
# 			msg = f"不支持该类型的提取方式:{method}"
# 			raise ValueError(msg)
# 		return cls.methods[method]()
