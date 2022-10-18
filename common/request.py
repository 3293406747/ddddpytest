import json
from json import JSONDecodeError
import allure
import requests
from pathlib import Path
from common.config import read_config
from common.logger import logger
from common.case import sqlSelect, assertion, extractVariable, renderTemplate, dynamicLoad
from common.variable import variable

__all__ = ["autoSendRequest", "send_request"]

path = Path(__file__).resolve()
session = requests.session()

def autoSendRequest(caseinfo):
	""" 获取用例自动发送请求 """
	variable.set("base_url",read_config()["base_url"])
	caseinfo = renderTemplate(caseinfo)
	caseinfo = dynamicLoad(caseinfo)
	temp = dict(
		url=caseinfo["request"].pop("url"),
		method=caseinfo["request"].pop("method"),
		files=caseinfo["request"].pop("files") if caseinfo["request"].get("files") else None,
		name=caseinfo["name"]
	)
	temp['url'] = caseinfo['base_url'] + temp['url'] if caseinfo['base_url'] else temp['url']
	if temp['files']:
		for k, v in temp['files'].items():
			temp['files'][k] = open(v, "rb")

	response = send_request(**temp, **caseinfo["request"])
	response = extractVariable(caseinfo,response)
	response = sqlSelect(caseinfo,response)
	response = assertion(caseinfo,response)
	return response

def logFixture(func):
	""" 日志记录 """
	def wapper(method, url, files=None, name=None, **kwargs):
		logger.info(f"{'接口请求开始':-^20}")
		logger.info(f"请求名称:{name}")
		logger.info(f"请求url:{url}")
		logger.info(f"请求方法:{method}")
		logger.info(f"请求参数:{kwargs}")
		logger.info(f"文件上传:{files}")
		response = func(method, url, name,files, **kwargs)
		logger.info(f"{'接口请求结束':-^20}")
		return response
	return wapper


def allureFixture(func):
	""" allure记录 """
	def wapper(method, url, files=None,name=None, **kwargs):
		allure.attach(body=url, name="请求url:", attachment_type=allure.attachment_type.TEXT)
		allure.attach(body=method, name="请求方式:", attachment_type=allure.attachment_type.TEXT)
		allure.attach(body=json.dumps(kwargs, ensure_ascii=False), name="请求参数:",
					  attachment_type=allure.attachment_type.TEXT)
		if files:
			allure.attach(body=json.dumps(files, ensure_ascii=False), name="文件上传:",
						  attachment_type=allure.attachment_type.TEXT)
		response = func(method, url, files,name,**kwargs)
		allure.attach(body=str(response.status_code), name="响应状态码:", attachment_type=allure.attachment_type.TEXT)
		data = None
		try:
			data = json.dumps(response.json(), ensure_ascii=False)
		except JSONDecodeError:
			response.encoding = "utf-8"
			data = response.text
		finally:
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


@allureFixture
@logFixture
def send_request(method, url, name,files=None, **kwargs):
	""" 发送同一个session请求 """
	response = session.request(method=method, url=url, files=files, timeout=10, **kwargs)
	return response