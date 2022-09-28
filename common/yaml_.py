import os.path
import yaml
from jinja2 import FileSystemLoader, Environment
from pathlib import Path

__all__ = ["read_testcase", "read_config"]

path = Path(__file__).resolve()
instance = {}


def analyze_testcase_format(function):
	""" 校验用例格式 """

	def wapper(file):
		cases = function(file)
		for case in cases:
			for x in ["name", "base_url", "request", "validata"]:
				if x not in dict(case).keys():
					raise Exception("yaml用例必须有的四个一级关键字: name,base_url,request,validata") from None
				if x == "request":
					for y in ["url", "method"]:
						if y not in dict(case)["request"].keys():
							raise Exception("yaml用例在request一级关键字下必须包括两个二级关键字:method,url") from None
		return cases

	return wapper


def dynamic_load(function):
	""" 热加载+获取项目环境地址 """

	def wapper(file):
		function(file)
		if not instance.get("env"):
			env = Environment(loader=FileSystemLoader(path.parent.parent))
			module = __import__("dynamic_load", fromlist=True)
			for func in read_config()["dynamic_load"]:
				env.globals[func] = getattr(module, func)
			instance['env'] = env
		temp = instance['env'].get_template(os.path.join("testcase", file).replace("\\", "/")).render(
			base_url=read_config()["base_url"])
		return yaml.load(stream=temp, Loader=yaml.FullLoader)

	return wapper


@dynamic_load
@analyze_testcase_format
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
