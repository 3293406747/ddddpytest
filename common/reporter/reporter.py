from abc import ABC, abstractmethod
import openpyxl


class Report(ABC):

	@abstractmethod
	def handle_data(self, data):
		pass

	@abstractmethod
	def write_to_container(self, data):
		pass

	@abstractmethod
	def save(self, file_path):
		pass


class ExcelReport(Report):

	def __init__(self):
		self.wb = openpyxl.Workbook()
		self.ws = self.wb.active

		columns_title = ('用例名称', '请求url', '请求方式', '请求参数', '响应状态码', '响应结果类型', '响应结果', '断言方式', '预期结果', '实际结果', '断言结果')
		self.ws.append(columns_title)

		self.failed_number = 0
		self.failed_casenames = []
		self.all_number = 0

	def handle_data(self, data):
		# 获取断言数据
		asserted_data_list = data.pop("断言")

		# 存放断言方法 断言预期值 断言实际值 断言结果
		method_array = []
		expect_array = []
		actual_array = []
		result_array = []

		# 遍历断言数据列表 asserted_data_list = [{},{}]
		for i, asserted_data in enumerate(asserted_data_list):
			# 标记 1. 2. 3.
			i += 1
			mark = str(i) + ". "

			# 获取method和value asserted_data = {method: ..., value: ...}
			assert_method = asserted_data['method']
			assert_value = asserted_data['value']

			# 存放二级断言预期结果 二级断言实际结果 二级断言结果
			sub_expect_array = []
			sub_actual_array = []
			sub_result_array = []

			n = 0

			# 遍历value中的元素 assert_value = {expect: ..., actual: ...,result: ...}
			for j, sub_item in enumerate(assert_value):
				# 二级标记 1.1 1.2 1.3 2.1
				j += 1
				sub_mark = "{}.{} ".format(str(i), str(j))

				# 获取expect、actual、result
				expect = sub_item.get('expect', [])
				actual = sub_item.get('actual', [])
				result = sub_item.get('result')

				# 二级断言预期结果添加内容：二级标记+,连接的字符串预期结果 [1.1 expect1,]
				sub_expect_array.append(sub_mark + ",".join(expect))
				# 二级断言结果添加内容：二级标记+结果 [1.1 result1,]
				sub_result_array.append(sub_mark + result)
				# 二级断言实际结果添加内容：二级标记+,连接的字符串实际结果 [1.1 actual,]
				if isinstance(actual, list):
					sub_actual_array.append(sub_mark + ",".join(actual))
				elif isinstance(actual, str):
					sub_actual_array.append(sub_mark + actual)

				n = j

			# 获取用例名称
			case_name = data.get("用例名称")

			# 如果二级断言结果中有断言失败, 失败用例数加1 记录失败用例名称
			if "断言失败，" in ",".join(sub_result_array):
				self.failed_number += 1
				self.failed_casenames.append(case_name)

			# 断言方法列表添加标记+断言方法+换行	[1. assert_method]
			method_array.append(mark + assert_method + "\n" * n)
			expect_array.append("\n".join(sub_expect_array) + "\n")
			actual_array.append("\n".join(sub_actual_array) + "\n")
			result_array.append("\n".join(sub_result_array) + "\n")
		return method_array, expect_array, actual_array, result_array

	def write_to_container(self, data):
		# 获取处理后的一行数据
		method_array, expect_array, actual_array, result_array = self.handle_data(data)

		# 将用例输入插入excel表格的一行中
		self.ws.append(
			[*data.values(), "\n".join(method_array), '\n'.join(expect_array), '\n'.join(actual_array),
			 "\n".join(result_array)]
		)
		# 记录用例总数
		self.all_number += 1

	def pre_save(self):
		# 用例执行数，失败数插入excel表格中
		self.ws.append([f"用例执行共{str(self.all_number)}条，失败共{str(self.failed_number)}条"])
		# 失败用例名称插入excel表格中
		if self.failed_casenames:
			self.ws.append([f"失败用例名称如下：{','.join(self.failed_casenames)}"])

		# 设置单元格自动换行选项和对齐方式
		for column_cells in self.ws.columns:
			for elem in column_cells:
				elem.alignment = openpyxl.styles.Alignment(vertical='top', horizontal='left', wrapText=False)

	def save(self, file_path):
		# 保存excel内容
		self.wb.save(file_path)

	def close(self):
		# 关闭Workbook对象
		self.wb.close()
