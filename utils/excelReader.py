"""
读取excel文件
"""
from openpyxl import load_workbook


def ExcelReader(file, sheet=None):
	""" 读取excel文件 """
	wb = load_workbook(filename=file, read_only=True)
	ws = wb[sheet] if sheet else wb.active
	rows = ws.values		# 生成器 生成每一行数据
	columns = next(rows)
	return [dict(zip(columns, row)) for row in rows]
	# column = next(ws.iter_rows(values_only=True))
	# return [dict(zip(column, row)) for row in ws.iter_rows(min_row=2, values_only=True)]
