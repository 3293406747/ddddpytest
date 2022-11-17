import yaml,csv
from pathlib import Path


path = Path(__file__).resolve().parent.parent
instance = {}

def read_config(file_name="local.yaml",encoding="utf-8") ->dict:
	""" 读取配置文件 """
	return Factory.create(method="config",file_name=file_name,encoding=encoding)

def read_data(file_name, encoding='utf-8'):
	""" 读取测试数据 """
	return Factory.create(method="data",file_name=file_name,encoding=encoding)

def read_case(file_name, encoding='utf-8'):
	""" 读取测试用例 """
	return Factory.create(method="testcase",file_name=file_name,encoding=encoding)


class Factory:

	@classmethod
	def create(cls,method,file_name,encoding):
		if method == "config":
			if not instance.get(file_name):
				with path.joinpath("config").joinpath(file_name).open(encoding=encoding) as f:
					data = yaml.load(stream=f, Loader=yaml.FullLoader)
				instance[file_name] = data
			return instance[file_name]
		elif method == "testcase":
			with path.joinpath("testcase").joinpath(file_name).open(encoding=encoding) as f:
				case = yaml.load(stream=f, Loader=yaml.FullLoader)
			return case
		elif method == "data":
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
		else:
			msg = "不支持该方法。"
			raise Exception(msg)
