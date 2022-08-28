import json
import os
import re
from typing import Union
import yaml
import pandas as pd
from utils.logger_util import logger

__all__ = ["Text", "Json", "Yaml", "Csv"]


class File:

	def __init__(self):
		self.file_path = ""
		self.exp = ""

	@logger.catch()
	def _pre_able(self, action: str) -> None:
		""" 校验文件是否存在，校验文件格式是否正确。"""
		fileable = os.path.exists(self.file_path)
		reformat = re.findall(self.exp, self.file_path)
		if not fileable or not reformat:
			raise Exception("您需要%s的文件在data目录下不存在或文件格式错误" % action) from None

	@logger.catch()
	def delete(self, filename: str) -> None:
		""" 删除文件 """
		self.file_path = filename
		self._pre_able("删除")
		os.remove(self.file_path)
		logger.success( "文件%s已成功被删除" % filename)


class Text(File):
	""" 操作文本文件，文件类型包括text、txt """

	def __init__(self):
		super().__init__()
		self.exp = r"^.*?\.te?xt$"

	@logger.catch()
	def _write(self, obj: Union[list, str], mode: str, start="") -> None:
		"""
		写入文件
		:param obj: 写入的内容
		:param mode:  写入模式
		:param start: 写入的文字开始字符
		:return:
		"""
		with open(self.file_path, mode, encoding="utf-8") as f:
			if isinstance(obj, list):
				text = start + "\n".join(obj)
			elif isinstance(obj, str):
				text = start + obj
			f.write(text)

	@logger.catch()
	def read(self, filename: str) -> list:
		""" 读取file目录下的文件 """
		self.file_path = filename
		self._pre_able("读取")
		lines = []
		with open(self.file_path, "r", encoding="utf-8") as file:
			for Line in file.readlines():
				l = Line.strip()
				lines.append(l)
		return lines

	@logger.catch()
	def write(self, filename: str, obj: Union[list, str]) -> None:
		"""
		将内容写入指定文件 文件必须不存在时才能写入，若文件已存在，请调用append方法。
		:param filename: 要写入的文件名
		:param obj: 要写入的内容，可以为列表或字符串
		:return: 写入成功的信息
		"""
		self.file_path = filename
		fileable = os.path.exists(self.file_path)
		reformat = re.findall(self.exp, self.file_path)
		if fileable or not reformat:
			raise FileNotFoundError("要写入的文件已存在或文件格式错误") from None
		self._write(obj, "w")
		logger.success("文本已成功写入文件%s中" % filename)

	@logger.catch()
	def append(self, filename: str, obj: Union[list, str]) -> None:
		"""
		将内容写入指定文件  文件必须存在时才能写入，若文件不存在，请调用write方法。
		:param filename: 要写入的文件名
		:param obj: 要写入的内容
		:return: 写入成功的信息
		"""
		self.file_path = filename
		self._pre_able("追加写入")
		self._write(obj, "a", start="\n")
		logger.success("文本已成功写入文件%s中" % filename)


class Json(File):

	def __init__(self):
		super(Json, self).__init__()
		self.exp = r"^.*?\.json$"

	@logger.catch()
	def read(self, filename: str) -> dict:
		""" 读取json文件 """
		self.file_path = filename
		self._pre_able("读取")
		with open(self.file_path, "r", encoding="utf-8") as f:
			j = json.load(f)
		return j

	@logger.catch()
	def write(self, filename, target: Union[dict, list]) -> None:
		""" 写入json文件  文件必须不存在时才能写入。"""
		self.file_path = filename
		fileable = os.path.exists(self.file_path)
		reformat = re.findall(self.exp, self.file_path)
		if fileable or not reformat:
			raise FileNotFoundError("要写入的文件已存在或文件格式错误") from None
		else:
			with open(self.file_path, "w", encoding="utf-8") as f:
				json.dump(target, f, indent=4, ensure_ascii=False)
		logger.success("文本已成功写入文件%s中" % filename)


class Yaml(File):
	def __init__(self):
		super().__init__()
		self.exp = r"^.*?\.yaml$"

	@logger.catch()
	def read(self, filename) -> list:
		""" 读取yaml文件 """
		self.file_path = filename
		self._pre_able("读取")
		with open(self.file_path, "r", encoding="utf-8") as f:
			# y = yaml.FullLoader(f).get_data()  两种方法均能读取
			y = yaml.load(f, yaml.FullLoader)
		return y


class Csv(File):

	def __init__(self):
		super(Csv, self).__init__()
		self.exp = r"^.*?\.csv$"

	@logger.catch()
	def read(self, filename: str) -> dict:
		""" 读取csv文件 """
		self.file_path = filename
		self._pre_able("读取")
		p = pd.read_csv(self.file_path, encoding="utf-8")
		return p

	@logger.catch()
	def append(self, filename, obj: Union[dict, list]) -> None:
		"""
		写入csv文件 文件必须存在时才能写入，若文件不存在，请调用write方法。
		:param filename: 要写入的文件名
		:param obj: 要写入的内容
		:return:  写入成功的提示信息
		"""
		self.file_path = filename
		fileable = os.path.exists(self.file_path)
		reformat = re.findall(self.exp, self.file_path)
		if not fileable or not reformat:
			raise FileNotFoundError("要写入的文件不存在或文件格式错误") from None
		else:
			p = pd.DataFrame(obj)
			p.to_csv(self.file_path, mode='a', index=False, header=False)
		logger.success("文本已成功写入文件%s中" % filename)

	@logger.catch()
	def write(self, filename, obj: Union[dict, list]) -> None:
		"""
		写入csv文件 文件必须不存在时才能写入，若文件存在，请调用append方法。
		:param filename: 要写入的文件名
		:param obj: 要写入的内容
		:return: 写入成功的提示信息
		"""
		self.file_path = filename
		fileable = os.path.exists(self.file_path)
		reformat = re.findall(self.exp, self.file_path)
		if fileable or not reformat:
			raise FileNotFoundError("要写入的文件已存在或文件格式错误") from None
		else:
			p = pd.DataFrame(obj)
			p.to_csv(self.file_path, mode='w', index=False, header=True)
		logger.success("文本已成功写入文件%s中" % filename)