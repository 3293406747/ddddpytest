import os.path
import yaml
from jinja2 import FileSystemLoader, Environment

__all__ = ["read_testcase", "read_extract", "read_config", "write_extract", "clear_extract"]

base_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
case_path = os.path.join(base_path, "testcase")
extract_path = os.path.join(base_path, "extract.yaml")
conf_path = os.path.join(base_path, "config.yaml")


def read_testcase(file):
	""" 读取测试用例 """
	case = os.path.join(case_path, file)
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
						raise Exception("yaml用例在request一级关键字下必须包括两个二级关键字:method,url")
		else:
			raise Exception("yaml用例必须有的四个一级关键字: name,base_url,request,validata")


def dynamic_load(filename):
	""" 热加载+获取项目环境地址 """
	env = Environment(loader=FileSystemLoader(base_path))
	module = __import__("dynamic_load", fromlist=True)
	for func in read_config()["dynamic_load"]:
		env.globals[func] = getattr(module, func)
	temp = env.get_template("/testcase/" + filename).render(base_url=read_config()["base_url"])
	load_yaml_text = yaml.load(stream=temp, Loader=yaml.FullLoader)
	return load_yaml_text


def read_extract():
	""" 读取extract """
	with open(file=extract_path, mode="r", encoding="utf-8") as f:
		yaml_text = yaml.load(stream=f, Loader=yaml.FullLoader)
		return yaml_text


def write_extract(data):
	""" 写入extract """
	with open(file=extract_path, mode="a", encoding="utf-8") as f:
		yaml.dump(data=data, stream=f, allow_unicode=True)


def clear_extract():
	""" 清空extract """
	with open(file=extract_path, mode="w", encoding="utf-8") as f:
		f.truncate()


def read_config():
	""" 读取config """
	with open(file=conf_path, mode="r", encoding="utf-8") as f:
		response = yaml.load(stream=f, Loader=yaml.FullLoader)
		return response
