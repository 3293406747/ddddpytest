import json,re
from string import Template
from typing import Pattern
from functools import partial
from common.case.factory import Factory
from common.case.parse import parse
from utils.variables import Variables
from common.variable.environments import Environments
from common.variable.globals import Globals

pattern: Pattern = re.compile(r"\{\{(.*?)\}\}")


def renderTemplate(data):
	""" 渲染模板 """
	data = json.dumps(data, ensure_ascii=False)
	# 使用变量
	merge = {**Variables().pool, **Globals().pool, **Environments().pool}
	# merge = Variables().pool | Globals().pool | Environments().pool
	genData = partial(Factory.create,mapping=merge)		# 构造偏函数
	data = genData(method="vary",obj=data)
	data = Template(json.dumps(data,ensure_ascii=False)).safe_substitute(merge)
	# 调用python函数
	data = genData(method="func", obj=data)
	data = pattern.sub(repl=parse, string=json.dumps(data,ensure_ascii=False))
	return json.loads(data)