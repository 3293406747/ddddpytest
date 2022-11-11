import json
import re
from json import JSONDecodeError
from string import Template
import allure
from common.assertion import Assertion
from common.extract import extractVariable
from common.read import read_config
from common.variable import Variables
from common.case import renderTemplate
from common.logger import logger
from common.response import Response
from common.session import session


def autoRequest(caseinfo, timeout=10):
	""" 自动请求 """
	# 设置base_url为变量
	if not Variables().get("base_url"):
		Variables().set(key="base_url", value=read_config()["base_url"])
	# 渲染请求
	newRequest = renderTemplate(caseinfo["request"])
	# 获取session
	sess = caseinfo.get("session")
	# 获取用例名称
	name = caseinfo["casename"]
	# 发送请求
	response = request(**newRequest, name=name, sess=sess, timeout=timeout)
	# 从请求或响应中提取内容:
	extractPool = {}
	if caseinfo.get("extract"):
		for who, val in caseinfo["extract"].items():
			for key, pattern in val.items():
				temp = str(pattern).split(",")
				pattern = temp.pop(0)
				index = int(temp[0]) if temp else None
				if pattern[0] == "$":
					# json提取
					value = extractVariable.json(data=newRequest if who == "request" else response.json(), expr=pattern,
												 index=index)
				else:
					# 正则提取
					try:
						data = response.json()
					except JSONDecodeError:
						data = response.text
					value = extractVariable.match(data=newRequest if who == "request" else data, pattern=pattern,
												  index=index)
				extractPool[key] = value
	# 断言
	if isinstance(caseinfo.get("assertion"), dict):
		# 使用从请求中提取的内容进行渲染
		temp = Template(json.dumps(caseinfo.get("assertion"), ensure_ascii=False)).safe_substitute(extractPool)
		# 渲染
		data = renderTemplate(temp)
		data = json.loads(data)
		for method, value in data.items():
			# 相等或不相等断言
			if method in ["equal", "unequal"]:
				for item in value:
					expect = re.sub(r"\[?\s?'(.*?)'\]?", r"\1", dict(item).get("expect")).split(",")
					actual = re.sub(r"\[?\s?'(.*?)'\]?", r"\1", dict(item).get("actual")).split(",")
					name = dict(item).get("name")
					if method == "equal":
						Assertion.equal(expect=expect, actual=actual,name=name)
					else:
						Assertion.unequal(expect=expect, actual=actual,name=name)
			# 包含或不包含断言
			elif method in ["contain", "uncontain"]:
				try:
					actual = response.json()
				except JSONDecodeError:
					actual = response.text
				for expect in value:
					if method == "contain":
						Assertion.contian(expect=expect, actual=actual)
					else:
						Assertion.uncontian(expect=expect,actual=actual)
	return response


class fixture:

	@classmethod
	def logfixture(cls, func):
		""" 日志记录 """

		def wapper(url, name, files=None, sess=None, timeout=10, method=None, **kwargs):
			logger.info(f"{'start':*^80s}")
			logger.info(f"请求名称:{name:.255s}")
			logger.info(f"请求url:{url:.255s}")
			if method:
				logger.info(f"请求方式:{method}")
			logger.info(f"请求参数:{json.dumps(kwargs, ensure_ascii=False):.255s}")
			if files:
				logger.info(f"文件上传:{json.dumps(files, ensure_ascii=False):.255s}")
			real = func(url=url, files=files, sess=sess, timeout=timeout, method=method, **kwargs)
			try:
				data = json.dumps(real.json(), ensure_ascii=False)
			except JSONDecodeError:
				data = real.text
			logger.info(f"响应结果:{data:.255s}")
			logger.info(f"{'end':*^80s}")
			return real

		return wapper

	@classmethod
	def files(cls, func):
		""" 文件处理 """

		def wapper(url, sess=None, method=None, files=None, timeout=10, **kwargs):
			if isinstance(files, dict):
				for file, path in files.items():
					files[file] = open(path, "rb")
			real = func(url=url, sess=sess, method=method, files=files, timeout=timeout, **kwargs)
			return real

		return wapper

	@classmethod
	def allure(cls, func):
		""" allure记录 """

		def wapper(url, sess=None, method=None, files=None, timeout=10, **kwargs):
			allure.attach(body=url, name="请求url:", attachment_type=allure.attachment_type.TEXT)
			if method:
				allure.attach(body=method, name="请求方式:", attachment_type=allure.attachment_type.TEXT)
			allure.attach(body=json.dumps(kwargs, ensure_ascii=False), name="请求参数:",
						  attachment_type=allure.attachment_type.TEXT)
			if files:
				allure.attach(body=json.dumps(files, ensure_ascii=False), name="文件上传:",
							  attachment_type=allure.attachment_type.TEXT)
			response = func(method=method, url=url, sess=sess, files=files, timeout=timeout, **kwargs)
			allure.attach(body=str(response.status_code), name="响应状态码:", attachment_type=allure.attachment_type.TEXT)
			try:
				data = json.dumps(response.json(), ensure_ascii=False)
			except JSONDecodeError:
				data = response.text
			allure.attach(body=data, name="响应数据:", attachment_type=allure.attachment_type.TEXT)
			if isinstance(response.content, bytes) and response.headers.get("Content-Type"):
				ct = response.headers["Content-Type"]
				if ct == "image/jpeg":
					allure.attach(body=response.content, name="image", attachment_type=allure.attachment_type.JPG)
				elif ct == "image/png":
					allure.attach(body=response.content, name="image", attachment_type=allure.attachment_type.PNG)
				elif ct == "application/pdf":
					allure.attach(body=response.content, name="pdf", attachment_type=allure.attachment_type.PDF)
			return response

		return wapper


@fixture.allure
@fixture.logfixture
@fixture.files
def request(method, url, files=None, sess=None, timeout=10, **kwargs):
	""" 发送请求 """
	response = session(seek=sess).request(method=method, url=url, files=files, timeout=timeout, **kwargs)
	return Response(response)


def get(url, files=None, sess=None, timeout=10, **kwargs):
	""" 发送get请求 """
	response = session(seek=sess).get(url=url, files=files, timeout=timeout, **kwargs)
	return Response(response)


def post(url, files=None, sess=None, timeout=10, **kwargs):
	""" 发送post请求 """
	response = session(seek=sess).post(url=url, files=files, timeout=timeout, **kwargs)
	return Response(response)
