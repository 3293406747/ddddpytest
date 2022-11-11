import json
from string import Template
import yaml
from common import request,function
from common.case import verifyCase
from common.variable import Variables,Globals,Environment
from common.session import session
from common.thread import thread
from common.assertion import Assertion
from common.read import read_data, read_config,read_case
from common.extract import extractVariable


class dp:

	@classmethod
	def requests(cls):
		""" 发送请求 """
		return request

	@classmethod
	def function(cls):
		""" python方法 """
		return function

	@classmethod
	def read_testcase(cls,file_name,item=0,encoding="utf-8"):
		""" 读取测试用例 """
		caseinfo = read_case(file_name=file_name, encoding=encoding)[item]
		caseinfo = verifyCase(caseinfo)
		if not caseinfo.get("data_path"):
			return [caseinfo]
		data_path = caseinfo.pop("data_path")
		caseinfo = json.dumps(caseinfo, ensure_ascii=False)
		caseList = []
		data = read_data(data_path)
		for i in data:
			temp = Template(caseinfo).safe_substitute(i)
			newCase = yaml.load(stream=temp, Loader=yaml.FullLoader)
			caseList.append(newCase)
		return caseList

	@classmethod
	def asserion(cls):
		""" 断言 """
		return Assertion

	@classmethod
	def variables(cls):
		""" 变量 """
		return Variables()

	@classmethod
	def globals(cls):
		""" 全局变量 """
		return Globals()

	@classmethod
	def environment(cls):
		""" 环境变量 """
		return Environment()

	@classmethod
	def read_data(cls, file_name, encoding="utf-8"):
		""" 读取case for csv文件"""
		return read_data(file_name=file_name, encoding=encoding)

	@classmethod
	def session(cls):
		""" session """
		return session

	@classmethod
	def thread(cls):
		""" 多线程装饰器 """
		return thread

	@classmethod
	def extractVariable(cls):
		""" 提取 """
		return extractVariable