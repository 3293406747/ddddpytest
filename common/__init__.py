from common import function
from common.request import autoRequest
from common.case import verifyCase, renderTemplate
from common.variable import Variables,Globals,Environment
from common.session import session
from common.thread import thread
from common.assertion import Assertion
from common.read import read_testcase
from common.extract import extract


class dp:

	@classmethod
	def autoRequest(cls,caseinfo,timeout=10):
		""" 发送请求 """
		return autoRequest(caseinfo=caseinfo,timeout=timeout)

	@classmethod
	def read_testcase(cls,file_name,item=0,encoding="utf-8"):
		""" 读取测试用例 """
		return read_testcase(file_name=file_name,item=item,encoding=encoding)

	@classmethod
	def asserion(cls):
		""" 断言 """
		return Assertion

	@classmethod
	def extract(cls):
		""" 提取 """
		return extract

	@classmethod
	def render(cls,data):
		""" 渲染 """
		return renderTemplate(data)

	@classmethod
	def session(cls):
		""" session """
		return session

	@classmethod
	def function(cls):
		""" python方法 """
		return function

	@classmethod
	def thread(cls):
		""" 多线程装饰器 """
		return thread

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

