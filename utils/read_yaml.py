"""
读取yaml文件
"""
import yaml


def read_yaml(filename, encoding='utf-8'):
	""" 读取yaml文件 """
	with open(file=filename, encoding=encoding) as f:
		return yaml.safe_load(f)
		# return yaml.load(stream=f, Loader=yaml.FullLoader)