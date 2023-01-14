from utils.singleinstance import singleInstance


@singleInstance
class Variables:
	""" 变量 """

	def __init__(self):
		self.__pool = {}

	def set(self,key,value):
		""" 设置变量 """
		self.__pool[key] = value

	def get(self,key,default=None):
		""" 获取变量 """
		return self.__pool.get(key,default)

	def unset(self,key):
		""" 删除变量 """
		del self.__pool[key]

	def clear(self):
		""" 清空所有变量 """
		self.__pool.clear()

	@property
	def pool(self) ->dict:
		""" 获取所有变量 """
		return self.__pool