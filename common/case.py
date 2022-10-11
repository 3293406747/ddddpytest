import json
import re
from string import Template
from typing import Pattern
import jsonpath
import yaml
from common.assertion import AssertionFactory
from common.function import function
from common.logger import logger
from common.mock import mock
from common.mysql import Mysql
from common.variable import variable
from common.yaml import read_config, read_globals, read_environment

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
			config = read_config("mysql")
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
	if not case['validata'] or not isinstance(case['validata'], dict):
		return response
	for sqls in case['validata'].values():
		if isinstance(sqls, list):
			for index, sql in enumerate(sqls):
				if isinstance(sql, str) and pattern.search(sql):
					sqls[index] = pattern.sub(RegexSql().select, sql)
		elif isinstance(sqls, dict):
			for key, sql in sqls.items():
				if isinstance(sql, str) and pattern.search(sql):
					sqls[key] = pattern.sub(RegexSql().select, sql)
	return response


def assertion(case, response):
	""" 响应断言 """
	if not isinstance(case["validata"], dict):
		return response
	for k, v in case["validata"].items():
		x, y = str(k).split("|")
		factory = AssertionFactory(x)
		if isinstance(v, list):
			for patterns in v:
				temp = drawPatterns(patterns, response, factory)
				match y:
					case 'exist':
						temp.exist()
					case 'unexist':
						temp.unexist()
					case _:
						raise ValueError
		elif isinstance(v, dict):
			for patterns, expect in v.items():
				temp = drawPatterns(patterns, response, factory)
				match y:
					case 'equal':
						temp.equal(expect)
					case 'unequal':
						temp.unequal(expect)
					case _:
						raise ValueError
	return response


def drawPatterns(patterns, response, factory):
	""" 抽取出的patterns """
	match str(patterns).split('|'):
		case [target]:
			target, index = target, 0
		case [target, index]:
			target, index = target, int(index)
		case _:
			raise ValueError
	return factory.create(target, response, index=index)


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
		merge = variable.pool | read_globals() if isinstance(read_globals(), dict) else variable.pool
		merge = merge|read_environment() if isinstance(read_environment(),dict) else merge
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
