import os.path
import yaml
from jinja2 import FileSystemLoader, Environment
from pathlib import Path

__all__ = ["read_testcase", "read_config"]

path = Path(__file__).resolve()
instance = {}


def read_testcase(file):
	""" 读取测试用例 """
	case = path.parent.parent / 'testcase' / file
	with open(file=case, mode="r", encoding="utf-8") as f:
		yaml_text = yaml.load(stream=f, Loader=yaml.FullLoader)
	list(map(analyze_testcase_format, yaml_text))
	yaml_text = dynamic_load(file)
	return yaml_text


def analyze_testcase_format(caseinfo):
	""" 校验用例格式 """
	first_index = ["name", "base_url", "request", "validata"]
	second_index = ["url", "method"]
	for x in first_index:
		if x in dict(caseinfo).keys():
			if x == "request":
				for y in second_index:
					if y not in dict(caseinfo)["request"].keys():
						raise Exception("yaml用例在request一级关键字下必须包括两个二级关键字:method,url") from None
		else:
			raise Exception("yaml用例必须有的四个一级关键字: name,base_url,request,validata") from None


def dynamic_load(filename):
	""" 热加载+获取项目环境地址 """
	if not instance.get("env"):
		env = Environment(loader=FileSystemLoader(path.parent.parent))
		module = __import__("dynamic_load", fromlist=True)
		for func in read_config()["dynamic_load"]:
			env.globals[func] = getattr(module, func)
		instance['env'] = env
	temp = instance['env'].get_template(os.path.join("testcase", filename).replace("\\", "/")).render(
		base_url=read_config()["base_url"])
	load_yaml_text = yaml.load(stream=temp, Loader=yaml.FullLoader)
	return load_yaml_text

def read_config():
	""" 读取config """
	if not instance.get("conf"):
		with open(file=path.parent.parent / 'config.yaml', mode="r", encoding="utf-8") as f:
			response = yaml.load(stream=f, Loader=yaml.FullLoader)
			instance['conf'] = response
	return instance['conf']
