"""
读取csv文件
"""
import csv


def read_csv(file, encoding='utf-8'):
	""" 读取csv文件 """
	with open(file=file, encoding=encoding) as f:
		reader = csv.DictReader(f)		# 将每一行转换为一个字典 自动使用 CSV 文件的第一行作为列头
		return [dict(row) for row in reader]
