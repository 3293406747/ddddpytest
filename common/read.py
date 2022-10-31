import yaml,csv
from pathlib import Path


path = Path(__file__).resolve().parent.parent
instance = {}

def read_config(file_name="local.yaml",encoding="utf-8") ->dict:
	""" 读取配置文件 """
	if not instance.get(file_name):
		with path.joinpath("config").joinpath(file_name).open(encoding=encoding) as f:
			data = yaml.load(stream=f, Loader=yaml.FullLoader)
		instance[file_name] = data
	return instance[file_name]

def read_data(file_name, encoding='utf-8'):
	""" 读取测试数据 """
	with path.joinpath("data").joinpath(file_name).open(encoding=encoding) as f:
		reader = csv.reader(f)
		column = next(reader)
		cases = []
		for row in reader:
			case = dict(zip(column,row))
			cases.append(case)
	return cases

def read_case(file_name, encoding='utf-8'):
	""" 读取测试用例 """
	with path.joinpath("testcase").joinpath(file_name).open(encoding=encoding) as f:
		case = yaml.load(stream=f,Loader=yaml.FullLoader)
	return case