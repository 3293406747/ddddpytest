import os.path
import yaml
from jinja2 import FileSystemLoader, Environment
from pathlib import Path

__all__ = ["read_testcase", "read_extract", "read_config", "write_extract", "clear_extract"]

path = Path(__file__).resolve()

def read_testcase(file):
	""" 读取测试用例 """
	case = path.parent.parent/'testcase'/file
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
	env = Environment(loader=FileSystemLoader(path.parent.parent))
	module = __import__("dynamic_load", fromlist=True)
	for func in read_config()["dynamic_load"]:
		env.globals[func] = getattr(module, func)
	temp = env.get_template(os.path.join("testcase",filename).replace("\\","/")).render(base_url=read_config()["base_url"])
	load_yaml_text = yaml.load(stream=temp, Loader=yaml.FullLoader)
	return load_yaml_text


def read_extract():
	""" 读取extract """
	with open(file=path.parent.parent/'extract.yaml', mode="r", encoding="utf-8") as f:
		yaml_text = yaml.load(stream=f, Loader=yaml.FullLoader)
		return yaml_text


def write_extract(data):
	""" 写入extract """
	with open(file=path.parent.parent/'extract.yaml', mode="a", encoding="utf-8") as f:
		yaml.dump(data=data, stream=f, allow_unicode=True)


def clear_extract():
	""" 清空extract """
	with open(file=path.parent.parent/'extract.yaml', mode="w", encoding="utf-8") as f:
		f.truncate()


def read_config():
	""" 读取config """
	with open(file=path.parent.parent/'config.yaml', mode="r", encoding="utf-8") as f:
		response = yaml.load(stream=f, Loader=yaml.FullLoader)
		return response
