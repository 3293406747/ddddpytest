import json
import re
from string import Template
from typing import Pattern
import yaml
from common.variable import Variables, Globals, Environment
from common import function

pattern: Pattern = re.compile(r"\{\{(.*?)\}\}")
__all__ = ["useFunc","renderTemplate"]

def useFunc(case):
	""" 调用python函数 """
	data = json.dumps(case, ensure_ascii=False)
	data = pattern.sub(repl=parse, string=data)
	res = json.loads(data)
	return res

def renderTemplate(case):
	""" 渲染用例 """
	data = json.dumps(case, ensure_ascii=False)
	merge = Variables().pool | Globals().pool | Environment().pool
	temp = Template(data).safe_substitute(merge)
	return yaml.load(stream=temp, Loader=yaml.FullLoader)

def parse(reMatch):
	""" repl解析 """
	charset = []
	args = []
	funcName = None
	func = function
	value = reMatch.group(1)
	for i in str(value).split("."):
		for char in i:
			if char == "(":
				funcName = "".join(charset)
				charset.clear()
			elif char == ")":
				if charset:
					args.append("".join(charset))
				break
			elif char == ",":
				args.append("".join(charset))
				charset.clear()
			else:
				charset.append(char)
		if args:
			func = getattr(func,funcName)(*args)
		else:
			func = getattr(func, funcName)()
	if not isinstance(func,str):
		msg = f"function {value} must return a string"
		raise TypeError(msg)
	return func