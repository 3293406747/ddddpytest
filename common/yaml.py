import yaml
from pathlib import Path
from common.template import formatTemplate

__all__ = ["read_testcase", "read_config"]

path = Path(__file__).resolve()
instance = {}


@formatTemplate
def read_testcase(file):
	""" 读取测试用例 """
	case = path.parent.parent / 'testcase' / file
	with open(file=case, mode="r", encoding="utf-8") as f:
		return yaml.load(stream=f, Loader=yaml.FullLoader)

def read_config(item):
	""" 读取config """
	if not instance.get("conf"):
		with open(file=path.parent.parent / 'config.yaml', mode="r", encoding="utf-8") as f:
			response = yaml.load(stream=f, Loader=yaml.FullLoader)
		instance['conf'] = response
	config = instance['conf']
	if item == "environment":
		return config["config"]["environment"]
	elif config["config"][item]:
		return config[item][config["config"][item]]
	else:
		return None

def read_globals():
	""" 读取全局变量 """
	if not instance.get("globals"):
		with open(file=path.parent.parent / 'globals.yaml', mode="r", encoding="utf-8") as f:
			response = yaml.load(stream=f, Loader=yaml.FullLoader)
		instance['globals'] = response
	return instance['globals']

def read_environment() ->dict:
	""" 读取环境变量 """
	if not instance.get("environment"):
		if not read_config("environment"):
			raise Exception("未设置环境")
		filename = read_config("environment")+'.yaml'
		with open(file=path.parent.parent / filename, mode="r", encoding="utf-8") as f:
			response = yaml.load(stream=f, Loader=yaml.FullLoader)
		instance['environment'] = response
	return instance['environment']
