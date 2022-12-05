from common import function
from common.request.autoRequest import autoRequest
from common.case.verify import verify
from common.case.render import renderTemplate
from common.variable.variables import Variables
from common.variable.environments import Environments
from common.variable.globals import Globals
from common.session.session import session
from common.assertion.assertion import Assertion
from common.read.read_testcase import read_testcase
from common.extract import extract
from common.logger.logger import logger
from common.read.read_config import read_config


class dp:

	logger = logger

	@classmethod
	def autoRequest(cls,caseinfo,timeout=10):
		""" 发送请求 """
		return autoRequest(caseinfo=caseinfo,timeout=timeout)

	@classmethod
	def read_testcase(cls,file_name,item=0,encoding="utf-8"):
		""" 读取测试用例 """
		return read_testcase(filename=file_name, item=item, encoding=encoding)

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
		return Environments()

	@classmethod
	def read_config(cls,filename="local.yaml",encoding="utf-8"):
		return read_config(filename=filename,encoding=encoding)

