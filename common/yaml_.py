import os.path
import yaml
from jinja2 import FileSystemLoader, Environment
from pathlib import Path

__all__ = ["read_testcase", "read_config"]

path = Path(__file__).resolve()
instance = {}


def formatTestcase(function):
	""" 校验用例格式 """
	def wapper(file):
		cases = function(file)
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

@formatTestcase
def read_testcase(file):
	""" 读取测试用例 """
	case = path.parent.parent / 'testcase' / file
	with open(file=case, mode="r", encoding="utf-8") as f:
		return yaml.load(stream=f, Loader=yaml.FullLoader)

def read_config():
	""" 读取config """
	if not instance.get("conf"):
		with open(file=path.parent.parent / 'config.yaml', mode="r", encoding="utf-8") as f:
			response = yaml.load(stream=f, Loader=yaml.FullLoader)
		instance['conf'] = response
	return instance['conf']
