import json
import re
from string import Template

import jsonpath
import yaml


from common.assertion import AssertionFactory
from common.logger import logger
from common.mysql import Mysql
from common.yaml_ import read_config

extractPool = {}

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
			self.mysql = Mysql(**config)
			RegexSql.__init_flag = False

	def select(self,reMatch):
		""" sql查询 """
		match str(reMatch.group(1)).split(','):
			case [sql,key]:
				logger.debug(f'sql:{sql}')
				return self.mysql.select(sql)[0][key]
			case [sql,key,index]:
				logger.debug(f'sql:{sql}')
				return self.mysql.select(sql)[int(index)][key]
			case _:
				raise ValueError

def sqlSelect(template,response):
	""" sql查询 """
	if not template['validata'] or not isinstance(template['validata'],dict):
		return response
	for sqls in template['validata'].values():
		if isinstance(sqls,list):
			for index, sql in enumerate(sqls):
				if isinstance(sql, str) and re.search('%.*?%', sql):
					sqls[index] = re.sub(r'%(.*?)%', RegexSql().select, sql)
		elif isinstance(sqls,dict):
			for key,sql in sqls.items():
				if isinstance(sql,str) and re.search('%.*?%',sql):
					sqls[key] = re.sub(r'%(.*?)%',RegexSql().select,sql)
	return response

def assertion(template,response):
	""" 响应断言 """
	if not isinstance(template["validata"], dict):
		return response
	for k,v in template["validata"].items():
		x,y = str(k).split("|")
		factory = AssertionFactory(x)
		if isinstance(v,list):
			for patterns in v:
				temp = drawPatterns(patterns,response,factory)
				match y:
					case 'exist':
						temp.exist()
					case 'unexist':
						temp.unexist()
					case _:
						raise ValueError
		elif isinstance(v,dict):
			for patterns,expect in v.items():
				temp = drawPatterns(patterns, response, factory)
				match y:
					case 'equal':
						temp.equal(expect)
					case 'unequal':
						temp.unequal(expect)
					case _:
						raise ValueError
	return response

def drawPatterns(patterns,response,factory):
	""" 抽取出的patterns """
	match str(patterns).split('|'):
		case [pattern]:
			pattern, index = pattern, 0
		case [pattern, index]:
			pattern, index = pattern, int(index)
		case _:
			raise ValueError
	return factory.create(pattern, response, index=index)

def extractVariable(template,response):
	""" 提取响应中的内容作为变量 """
	if "extract" in template.keys():
		for key, value in template["extract"].items():
			if "(" in value and ")" in value:  # 正则提取器
				extract = re.search(value, response.text).group(1)
			elif "$" in value:  # json提取器
				extract = jsonpath.jsonpath(response.json(), value)[0]
			else:
				raise Exception("提取器表达式错误") from None
			extractPool[key] = extract
	return response

def renderTemplate(template):
	""" 渲染用例 """
	data = json.dumps(template,ensure_ascii=False) if isinstance(template, dict) else template
	if extractPool and data:
		temp = Template(data).safe_substitute(extractPool)
		return yaml.load(stream=temp, Loader=yaml.FullLoader)
	elif data:
		return yaml.load(stream=data, Loader=yaml.FullLoader)
	else:
		return None