from pathlib import Path
import yaml


path = Path(__file__).resolve().parent.parent.parent.joinpath('environment')

class Environments:
	""" 环境变量 """
	__instance = None
	__init_flag = True

	def __new__(cls):
		if cls.__instance is None:
			cls.__instance = object.__new__(cls)
			return cls.__instance
		else:
			return cls.__instance

	def __init__(self,file_name="local.yaml",encoding="utf-8"):
		if Environments.__init_flag:
			self.encoding = encoding
			self.file_name = file_name
			with path.joinpath(self.file_name).open(encoding=self.encoding) as f:
				self.__pool = yaml.load(stream=f, Loader=yaml.FullLoader) or {}
			Environments.__init_flag = False

	def set(self,key,value):
		""" 设置变量 """
		self.__pool[key] = value
		with path.joinpath(self.file_name).open(mode="w",encoding=self.encoding) as f:
			yaml.dump(data=self.__pool, stream=f)

	def get(self,key):
		""" 获取变量 """
		return self.__pool.get(key)

	def unset(self,key):
		""" 删除变量 """
		del self.__pool[key]
		with path.joinpath(self.file_name).open(mode="w",encoding=self.encoding) as f:
			yaml.dump(data=self.__pool, stream=f)

	def clear(self):
		""" 清空所有变量 """
		self.__pool.clear()
		with path.joinpath(self.file_name).open(mode="w", encoding=self.encoding) as f:
			f.truncate()

	@property
	def pool(self) -> dict:
		""" 获取所有变量 """
		return self.__pool