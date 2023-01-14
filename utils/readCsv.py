import csv


def read_csv(file, encoding='utf-8'):
	""" 读取csv文件 """
	with open(file=file, encoding=encoding) as f:
		reader = csv.reader(f)
		column = next(reader)
	return [dict(zip(column, row)) for row in reader]
