class Variable:

	def __init__(self):
		self.__pool = {}

	def set(self,key,value):
		self.__pool[key] = value

	def get(self,key):
		self.__pool.get(key, "null")

	def clear(self):
		self.__pool.clear()

	@property
	def pool(self):
		return self.__pool

	@property
	def is_empty(self):
		return self.__pool == {}

variable = Variable()