from pathlib import Path

path = Path(__file__).resolve().parent.parent.parent.joinpath('environment')


class Variables:
	""" 变量 """
	__instance = None
	__init_flag = True

	def __new__(cls):
		if cls.__instance is None:
			cls.__instance = object.__new__(cls)
			return cls.__instance
		else:
			return cls.__instance

	def __init__(self):
		if Variables.__init_flag:
			self.__pool = {}
			Variables.__init_flag = False


	def set(self,key,value):
		""" 设置变量 """
		self.__pool[key] = value

	def get(self,key):
		""" 获取变量 """
		return self.__pool.get(key)

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