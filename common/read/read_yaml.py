import yaml
from pathlib import Path


path = Path(__file__).resolve().parent.parent.parent

def read_yaml(filename, encoding='utf-8'):
	""" 读取测试用例 """
	with path.joinpath("testcase").joinpath(filename).open(encoding=encoding) as f:
		case = yaml.load(stream=f, Loader=yaml.FullLoader)
	return case