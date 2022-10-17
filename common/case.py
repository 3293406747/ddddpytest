import json
import re
from string import Template
from typing import Pattern
import jsonpath
import yaml
from common.assertion import AssertionFactory
from common.config import read_config
from common.function import function
from common.logger import logger
from common.mock import mock
from common.mysql import Mysql
from common.variable import variable, global_, environment

pattern: Pattern = re.compile(r"\{\{(.*?)\}\}")


class RegexSql:
	""" sql正则处理 """

	instance = None
	__init_flag = True

	def __new__(cls, *args, **kwargs):
		if cls.instance is None:
			cls.instance = object.__new__(cls)
			return cls.instance
		else:
			return cls.instance

	def __init__(self):
		if RegexSql.__init_flag:
			config = read_config()["mysql"]
			if not config:
				raise Exception("config.yaml中未配置数据库连接")
			self.mysql = Mysql(**config)
			RegexSql.__init_flag = False

	def select(self, reMatch):
		""" sql查询 """
		match str(reMatch.group(1)).split(','):
			case [sql, key]:
				logger.debug(f'sql:{sql}')
				return self.mysql.select(sql)[0][key]
			case [sql, key, index]:
				logger.debug(f'sql:{sql}')
				return self.mysql.select(sql)[int(index)][key]
			case _:
				raise ValueError


def sqlSelect(case, response):
	""" sql查询 """
	if not case['validata']:
		return response
	if not isinstance(case['validata'], list):
		raise TypeError(f"{case['validata']} must is a list")
	jsondata = json.dumps(case['validata'],ensure_ascii=False)
	if pattern.search(jsondata):
		temp = pattern.sub(RegexSql().select,jsondata)
		case['validata'] = json.loads(temp)
	return response


def assertion(case, response):
	""" 响应断言 """
	if not case["validata"]:
		return response
	elif not isinstance(case["validata"],list):
		raise TypeError("validata must is a list")
	else:
		elems = ["target","pattern","expect","index","name"]
		for i in case["validata"]:
			if not isinstance(i,dict):
				raise TypeError(f"{i} must is a dict")
			tflist = list(map(lambda x:True if x in elems else False,i.keys()))
			if not all(tflist):
				raise ValueError(f"{list(i.keys())} must in {elems}")
			AssertionFactory.create(**i,response=response)
	return response


def extractVariable(case, response):
	""" 提取响应中的内容作为变量 """
	if "extract" in case.keys():
		for key, value in case["extract"].items():
			if "(" in value and ")" in value:  # 正则提取器
				extract = re.search(value, response.text).group(1)
			elif "$" in value:  # json提取器
				extract = jsonpath.jsonpath(response.json(), value)[0]
			else:
				raise Exception("提取器表达式错误") from None
			variable.set(key, extract)
	return response


def renderTemplate(case):
	""" 渲染用例 """
	data = json.dumps(case, ensure_ascii=False) if isinstance(case, dict) else case
	if not variable.is_empty and data:
		merge = variable.pool | global_.pool | environment.pool
		temp = Template(data).safe_substitute(merge)

		return yaml.load(stream=temp, Loader=yaml.FullLoader)
	elif data:
		return yaml.load(stream=data, Loader=yaml.FullLoader)
	else:
		return None


class RegexFunctionMock:
	""" 函数及mock数据处理 """
	instance = None
	flag = True

	def __new__(cls, *args, **kwargs):
		if cls.instance is None:
			cls.instance = object.__new__(cls)
			return cls.instance
		else:
			return cls.instance

	def __init__(self):
		if RegexFunctionMock.flag:
			self.func = function
			self.mock = mock
			RegexFunctionMock.flag = False

	def main(self, reMatch):
		elems = reMatch.group(1).split("|")
		p = []
		for elem in elems:
			if str(elem).startswith("@"):
				attr, *args = str(elem).lstrip("@").split(",")
				p.append(getattr(self.mock, attr)(*args))
			elif str(elem).startswith("#"):
				attr, *args = str(elem).lstrip("#").split(",")
				if p:
					temp = getattr(self.func, attr)("".join(p), *args)
				else:
					temp = getattr(self.func, attr)(*args)
				p.clear()
				p.append(temp)
			else:
				p.append(str(elem))
		return "".join(p)


def dynamicLoad(case):
	"""
	函数及mock数据处理
	书写方式如：{{@cword|string1|#md5|string2|#md5}}
	"""
	data = json.dumps(case, ensure_ascii=False)
	data = pattern.sub(RegexFunctionMock().main, data)
	return yaml.load(data, yaml.FullLoader)
