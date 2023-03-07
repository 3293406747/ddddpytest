from abc import ABC, abstractmethod
import openpyxl
from openpyxl import Workbook


class Report(ABC):

	@abstractmethod
	def handle_data(self, data):
		pass

	@abstractmethod
	def write_to_container(self, data):
		pass


class ExcelReport(Report):

	def __init__(self, file_path):
		self.file_path = file_path
		self.wb = Workbook()
		self.ws = self.wb.active
		self.ws.append(['用例名称', '请求url', '请求方式', '请求参数', '响应结果类型', '响应结果', '断言方式', '预期结果', '实际结果', '断言结果'])

	def handle_data(self, data):
		assert_data = data.pop("断言")

		method_array = []
		expect_array = []
		actual_array = []
		result_array = []
		i = 0
		# 遍历数据
		for item in assert_data:
			i += 1
			mark = str(i) + ". "

			# 获取method和value
			method = item['method']
			value = item['value']

			sub_expect_array = []
			sub_actual_array = []
			sub_result_array = []
			j = 0
			# 遍历value中的元素
			for sub_item in value:
				j += 1
				sub_mark = str(i) + "." + str(j) + " "

				# 获取expect、actual、result
				expect = sub_item.get('expect', [])
				actual = sub_item.get('actual', [])
				result = sub_item.get('result')

				sub_expect_array.append(sub_mark + ",".join(expect))
				sub_result_array.append(sub_mark + result)
				if isinstance(actual, list):
					sub_actual_array.append(sub_mark + ",".join(actual))
				elif isinstance(actual, str):
					sub_actual_array.append(sub_mark + actual)

			method_array.append(mark + method + "\n" * j)
			expect_array.append("\n".join(sub_expect_array) + "\n")
			actual_array.append("\n".join(sub_actual_array) + "\n")
			result_array.append("\n".join(sub_result_array) + "\n")
		return method_array, expect_array, actual_array, result_array

	def write_to_container(self, data):
		method_array, expect_array, actual_array, result_array = self.handle_data(data)
		self.ws.append(
			[*data.values(), "\n".join(method_array), '\n'.join(expect_array), '\n'.join(actual_array),
			 "\n".join(result_array)]
		)

	def save(self):
		for column_cells in self.ws.columns:
			# 设置单元格自动换行选项和对齐方式
			for elem in column_cells:
				elem.alignment = openpyxl.styles.Alignment(vertical='top', horizontal='left', wrapText=True)

		self.wb.save(self.file_path)
