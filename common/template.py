import re
from typing import Pattern
from pathlib import Path
import yaml

from common.session import session

path = Path(__file__).resolve()
pattern: Pattern = re.compile(r"\{\{(.*?)\}\}")

def formatTemplate(func):
	""" 校验用例格式 """
	def wapper(template=None):
		cases = func(template) if template else func()
		if not cases:
			return cases
		elems = ["name", "base_url", "request", "validata"]
		for elem in elems:
			for case in cases:
				if elem not in case.keys():
					raise Exception("yaml用例必须有的四个一级关键字: name,base_url,request,validata") from None
				elif elem == "request":
					for item in ["url", "method"]:
						if item not in case["request"]:
							raise Exception("yaml用例在request一级关键字下必须包括两个二级关键字:method,url") from None
		return cases
	return wapper

@formatTemplate
def read_testcase(file):
	""" 读取测试用例 """
	case = path.parent.parent / 'testcase' / file
	with open(file=case, mode="r", encoding="utf-8") as f:
		return yaml.load(stream=f, Loader=yaml.FullLoader)

@formatTemplate
def login():
	case = path.parent.parent / 'testcase' / 'login.yaml'
	with open(file=case, mode="r", encoding="utf-8") as f:
		r = yaml.load(stream=f, Loader=yaml.FullLoader)
		session.generate_handle() if not r else [session.generate_handle() for _ in range(len(r))]
		return r