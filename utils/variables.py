"""
变量池
"""
from utils.singleinstance import singleton


@singleton
class Variables:
	""" 变量 """

	def __init__(self):
		self._pool = {}

	def set(self,key,value):
		""" 设置变量 """
		self._pool[key] = value

	def get(self,key,default=None):
		""" 获取变量 """
		return self._pool.get(key, default)

	def unset(self,key):
		""" 删除变量 """
		if key in self._pool:
			del self._pool[key]

	def clear(self):
		""" 清空所有变量 """
		self._pool.clear()

	@property
	def pool(self) ->dict:
		""" 获取所有变量 """
		return self._pool


variables = Variables()