import json
from string import Template
import yaml
from common import request,function
from common.variable import Variables,Globals,Environment
from common.session import session
from common.thread import thread
from common.assertion import Assertion
from common.response import Response
from common.case import useFunc
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
	def read_testcase(cls,file_name, item=0):
		""" 读取测试用例 """
		case_ = read_case(file_name=file_name)[item]
		if not case_.get("data_path"):
			return [case_]
		data_path = case_.pop("data_path")
		case_ = json.dumps(case_, ensure_ascii=False)
		caseList = []
		data = read_data(data_path)
		for i in data:
			temp = Template(case_).safe_substitute(i)
			newCase = yaml.load(stream=temp, Loader=yaml.FullLoader)
			caseList.append(newCase)
		return caseList

	@classmethod
	def asserion(cls):
		""" 断言 """
		return Assertion

	@classmethod
	def response(cls,res):
		""" 响应 """
		return Response(res)

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
	def useFunc(cls,data):
		""" 调用python函数 """
		return useFunc(data)

	@classmethod
	def extractVariable(cls):
		""" 提取 """
		return extractVariable