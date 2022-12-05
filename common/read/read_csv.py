import csv
from pathlib import Path

path = Path(__file__).resolve().parent.parent.parent

def read_csv(filename, encoding='utf-8'):
	""" 读取csv测试数据 已废弃 """
	with path.joinpath("data").joinpath(filename).open(encoding=encoding) as f:
		reader = csv.reader(f)
		column = next(reader)
		dataset = [dict(zip(column,row)) for row in reader]
	return dataset