"""
变量池
"""
from abc import ABC, abstractmethod
from pathlib import Path
import yaml
from utils.singleinstance import singleton


class VariablesManager(ABC):

	@abstractmethod
	def set(self, key, value):
		pass

	def get(self, key, default=None):
		pass

	def unset(self, key):
		pass

	def clear(self):
		pass

	def pool(self):
		pass


@singleton
class SystemVariablesManager(VariablesManager):
	""" 变量 """

	def __init__(self):
		self._pool = {}

	def set(self, key, value):
		""" 设置变量 """
		self._pool[key] = value

	def get(self, key, default=None):
		""" 获取变量 """
		return self._pool.get(key, default)

	def unset(self, key):
		""" 删除变量 """
		self._pool.pop(key, None)

	def clear(self):
		""" 清空所有变量 """
		self._pool.clear()

	@property
	def pool(self) -> dict:
		""" 获取所有变量 """
		return self._pool


ENVIRONMENT_DIR = Path(__file__).resolve().parent.parent.joinpath('environment')


@singleton
class FileVariablesManager(VariablesManager):
	""" 文件变量 """

	def __init__(self, file_name="local.yaml", encoding="utf-8"):
		self.encoding = encoding
		self.file_path = ENVIRONMENT_DIR.joinpath(file_name)
		with self.file_path.open(encoding=self.encoding) as f:
			self.__pool = yaml.safe_load(f) or {}

	def set(self, key, value):
		""" 设置变量 """
		self.__pool[key] = value
		with self.file_path.open(mode="a", encoding=self.encoding) as f:
			yaml.safe_dump(self.__pool, f)

	def get(self, key, default=None):
		""" 获取变量 """
		return self.__pool.get(key, default)

	def unset(self, key):
		""" 删除变量 """
		self.__pool.pop(key, None)
		with self.file_path.open(mode="a", encoding=self.encoding) as f:
			yaml.safe_dump(self.__pool, f)

	def clear(self):
		""" 清空所有变量 """
		self.__pool.clear()
		with self.file_path.open(mode="w", encoding=self.encoding) as f:
			f.write("")

	@property
	def pool(self) -> dict:
		""" 获取所有变量 """
		return self.__pool


variables = SystemVariablesManager()
environments = FileVariablesManager()