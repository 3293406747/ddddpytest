"""
读取yaml文件
"""
import yaml


def readYaml(file, encoding='utf-8'):
	""" 读取yaml文件 """
	with open(file=file,encoding=encoding) as f:
		return yaml.load(stream=f, Loader=yaml.FullLoader)