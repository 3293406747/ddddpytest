from common import request,function
from common.variable import Variables,Globals,Environment
from common.session import session
from common.thread import thread
from common.assertion import Assertion
from common.response import Response
from common.case import useFunc,renderTemplate
from common.read import read_data, read_config,read_case


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
		Variables().set(key="base_url",value=read_config()["base_url"])
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
	def use_func(cls,case_):
		""" case中调用python方法 """
		return useFunc(case=case_)

	@classmethod
	def renderTemplate(cls,case_):
		""" 渲染case """
		return renderTemplate(case=case_)

	@classmethod
	def case_parse(cls,case_):
		""" 解析case """
		data = dp.use_func(case_)
		data = dp.renderTemplate(data)
		return data

	@classmethod
	def read_data(cls, file_name, encoding="utf-8"):
		""" 读取case for csv文件"""
		return read_data(file_name=file_name, encoding=encoding)

	@classmethod
	def read_case(cls, file_name, encoding="utf-8"):
		""" 读取case for csv文件"""
		return read_case(file_name=file_name, encoding=encoding)

	@classmethod
	def session(cls):
		""" session """
		return session

	@classmethod
	def thread(cls):
		""" 多线程装饰器 """
		return thread