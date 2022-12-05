import requests


class Session:

	def __init__(self):
		self.__sessPool = []
		self.__seek = 0

	def new(self,item=1):
		""" 创建session对象 """
		for _ in range(item):
			sess = requests.session()
			self.__sessPool.append(sess)

	def __call__(self, seek=None) -> requests.Session:
		""" 返回session对象 """
		self.__seek = self.__seek if seek is None else seek
		return self.__sessPool[self.__seek]

	def clear(self):
		""" 清空session池 """
		self.__sessPool.clear()

	def __delitem__(self, key):
		""" 删除session """
		del self.__sessPool[key]

	@property
	def seek(self):
		""" session池中session指向 """
		return self.__seek

	@seek.setter
	def seek(self, item):
		""" 修改session池中session指向 """
		self.__seek = item

	def sessions(self):
		"""" 获取session池中所有session """
		return self.__sessPool


session = Session()
