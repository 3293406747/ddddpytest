from abc import ABC, abstractmethod
import aiohttp


class SessionManager(ABC):
	"""session管理器"""

	@abstractmethod
	def create_session(self, timeout: int = 10, *args, **kwargs):
		"""创建session"""
		pass

	@abstractmethod
	def get_session(self, index: int = 0, *args, **kwargs):
		"""获取session"""
		pass

	@abstractmethod
	def close_session(self, index: int = 0, *args, **kwargs):
		"""关闭session"""
		pass


class AsyncSessionManager(SessionManager):
	"""异步session管理器"""

	def __init__(self):
		self.sessionPool = []

	def create_session(self, timeout: int = 10, *args, **kwargs) -> aiohttp.ClientSession:
		formated_timeout = aiohttp.ClientTimeout(total=timeout)
		session = aiohttp.ClientSession(timeout=formated_timeout)
		self.sessionPool.append(session)
		return session

	def get_session(self, index: int = 0, *args, **kwargs) -> aiohttp.ClientSession:
		return self.sessionPool[index]

	def close_session(self, index: int = 0, *args, **kwargs) -> None:
		self.sessionPool[index].close()

	async def close_all_session(self) -> None:
		for session in self.sessionPool:
			await session.close()

	def clear_session_pool(self) -> None:
		""" 清空session池 """
		self.sessionPool.clear()

	def __delitem__(self, index: int) -> None:
		""" 删除session """
		del self.sessionPool[index]

	def __getitem__(self, index: int):
		""" 获取session池中的session """
		return self.sessionPool[index]

	def __setitem__(self, index: int, value):
		""" 修改session池中的session """
		self.sessionPool[index] = value


# class SessionManager:
#
# 	def __init__(self):
# 		self.__sessPool: [requests.Session] = []
# 		self.__seek = 0
#
# 	def create_session(self, item=1) -> None:
# 		""" 创建session对象 """
# 		for _ in range(item):
# 			sess = requests.session()
# 			self.__sessPool.append(sess)
#
# 	def __call__(self, seek: None | int = None) -> requests.Session:
# 		""" 返回session对象 """
# 		self.__seek = self.__seek if seek is None else seek
# 		return self.__sessPool[self.__seek]
#
# 	def clear(self) -> None:
# 		""" 清空session池 """
# 		self.__sessPool.clear()
#
# 	def __delitem__(self, key) -> None:
# 		""" 删除session """
# 		del self.__sessPool[key]
#
# 	@property
# 	def seek(self) -> int:
# 		""" session池中session指向 """
# 		return self.__seek
#
# 	@seek.setter
# 	def seek(self, item: int) -> None:
# 		""" 修改session池中session指向 """
# 		self.__seek = item
#
# 	def sessions(self) -> [requests.Session]:
# 		"""" 获取session池中所有session """
# 		return self.__sessPool
#
# 	def __len__(self) -> int:
# 		""" 获取session池中session的数量 """
# 		return len(self.__sessPool)
#
# 	def __getitem__(self, index: int) -> requests.Session:
# 		""" 获取session池中的session """
# 		return self.__sessPool[index]
#
# 	def __setitem__(self, index: int, value: requests.Session) -> None:
# 		""" 修改session池中的session """
# 		self.__sessPool[index] = value


# session = SessionManager()
asyncSession = AsyncSessionManager()
