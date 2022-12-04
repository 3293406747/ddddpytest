import json
from string import Template
import yaml,csv
from pathlib import Path
from common.case import verifyCase, renderTemplate

path = Path(__file__).resolve().parent.parent
instance = {}

def read_config(file_name="local.yaml",encoding="utf-8") ->dict:
	""" 读取配置文件 """
	if not instance.get(file_name):
		with path.joinpath("config").joinpath(file_name).open(encoding=encoding) as f:
			data = yaml.load(stream=f, Loader=yaml.FullLoader)
		instance[file_name] = data
	config = renderTemplate(instance[file_name])
	return config

def read_data(file_name, encoding='utf-8'):
	""" 读取测试数据 """
	with path.joinpath("data").joinpath(file_name).open(encoding=encoding) as f:
		reader = csv.reader(f)
		column = next(reader)
		cases = []
		for row in reader:
			row: list
			for i, val in enumerate(row):
				if val == "null":
					row[i] = None
			case = dict(zip(column, row))
			cases.append(case)
	return cases

def read_case(file_name, encoding='utf-8'):
	""" 读取测试用例 """
	with path.joinpath("testcase").joinpath(file_name).open(encoding=encoding) as f:
		case = yaml.load(stream=f, Loader=yaml.FullLoader)
	return case

def read_testcase(file_name,item=0,encoding="utf-8"):
	""" 读取测试用例 """
	caseinfo = read_case(file_name=file_name, encoding=encoding)[item]
	caseinfo = verifyCase(caseinfo)
	if not caseinfo.get("data_path"):
		return [caseinfo]
	data_path = caseinfo.pop("data_path")
	caseinfo = json.dumps(caseinfo, ensure_ascii=False)
	caseList = []
	data = read_data(data_path)
	for i in data:
		temp = Template(caseinfo).safe_substitute(i)
		newCase = yaml.load(stream=temp, Loader=yaml.FullLoader)
		caseList.append(newCase)
	return caseList
