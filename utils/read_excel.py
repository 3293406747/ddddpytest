"""
读取excel文件
"""
from openpyxl import load_workbook


def read_excel(filename, sheet=None):
	""" 读取excel文件 """
	wb = load_workbook(filename=filename, read_only=True)
	ws = wb[sheet] if sheet else wb.active
	rows = ws.values		# 生成器 生成每一行数据
	columns = next(rows)
	return [dict(zip(columns, row)) for row in rows]
