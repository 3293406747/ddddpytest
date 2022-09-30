import json
import re
import time
import allure
import jsonpath
import requests
import yaml
from common.logger import logger
from common.mysql import Mysql
from mako.template import Template
from pathlib import Path

__all__ = ["autoSendRequest", "send_request", "extract_variable"]

path = Path(__file__).resolve()
session = requests.session()
extractPool = {}


def sqlHandle(func):
	""" sql处理 """
	def wapper(caseinfo):
		response = func(caseinfo)
		if caseinfo["validata"]:
			p = r'select\s*(.*?)\sfrom'
			if caseinfo["validata"].get('equal'):
				for k, v in caseinfo["validata"]["equal"].items():
					if re.match(p, str(v)):
						res = Mysql().select(sql=v)
						key = re.match(p, v).group(1)
						caseinfo["validata"]["equal"][k] = res[0][key]
			if caseinfo["validata"].get('contain'):
				for i in range(len(caseinfo["validata"]['contain'])):
					if re.match(p, str(caseinfo["validata"]['contain'][i])):
						res = Mysql().select(sql=caseinfo["validata"]['contain'][i])
						key = re.match(p, caseinfo["validata"]['contain'][i]).group(1)
						caseinfo["validata"]['contain'][i] = res[0][key]
		return response
	return wapper


def extract_variable(func):
	""" 接口关联:提取响应中的内容 """
	def wapper(caseinfo):
		response = func(caseinfo)
		if "extract" in caseinfo.keys():
			for key, value in caseinfo["extract"].items():
				tf_list = list(map(lambda x: True if x in value else False, ["$", ">", "(", ")"]))
				if all(tf_list):  # json+正则提取器
					json_extract, re_extract = str(response.json()).split(">")
					temp = jsonpath.jsonpath(str(json_extract).strip(), value)[0]
					extract = re.search(str(re_extract).strip(), temp).group(1)
				elif "(" in value and ")" in value:  # 正则提取器
					extract = re.search(value, response.text).group(1)
				elif "$" in value:  # json提取器
					extract = jsonpath.jsonpath(response.json(), value)[0]
				else:
					raise Exception("提取器表达式错误") from None
				extractPool[key] = extract
		# 渲染validata
		caseinfo["validata"] = render_template(caseinfo["validata"])
		return response
	return wapper


def assertion(func):
	""" 响应断言 """
	def wapper(caseinfo):
		response = func(caseinfo)
		if isinstance(caseinfo["validata"], dict):
			for key, value in caseinfo["validata"].items():
				if key == "equal" and isinstance(value, dict):  # 相等断言
					equalFrame(value, response)
				elif key == "contain":
					containFrame(caseinfo["validata"]["contain"], response)  # 包含断言
		return response
	return wapper


@assertion
@sqlHandle
@extract_variable
def autoSendRequest(caseinfo):
	""" 获取用例自动发送请求 """
	temp = dict(
		url=caseinfo["request"].pop("url"),
		method=caseinfo["request"].pop("method"),
		base_url=caseinfo["base_url"],
		files=caseinfo["request"].pop("files") if caseinfo["request"].get("files") else None,
		name=caseinfo["name"]
	)
	response = send_request(**temp, **caseinfo["request"])
	return response


def render_template(data):
	""" 渲染用例 """
	data = json.dumps(data) if data and isinstance(data, dict) else data
	if extractPool and data:  # extract.yaml文件可能为空，为空时不渲染用例
		temp = Template(data).render(**extractPool)
		return yaml.load(stream=temp, Loader=yaml.FullLoader)
	elif not data:
		return None
	else:
		return yaml.load(stream=data, Loader=yaml.FullLoader)


def parameterHandle(func):
	""" 参数处理 """
	def wapper(method, url, base_url=None, files=None, **kwargs):
		method = str(method).lower()
		url = render_template(url)
		url = base_url + url if base_url else url
		# 配置中无base_url或者send_request方法不传入base_url参数，都会使base_url为None
		for key, value in kwargs.items():
			if key in ("headers", "params", "data", "json"):
				kwargs[key] = render_template(value)
		if files:
			for k, v in files.items():
				files[k] = open(v, "rb")
		return func(method, url, files, **kwargs)
	return wapper


def downloadFixture(func):
	""" 文件下载 """
	def wapper(method, url, files=None, **kwargs):
		response = func(method, url, files, **kwargs)
		flag = False
		if isinstance(response.content, bytes) and response.headers.get("Content-Type"):
			ct = response.headers["Content-Type"]
			if ct == "image/jpeg":
				flag = True
				allure.attach(body=response.content, name="jpeg图片", attachment_type=allure.attachment_type.JPG)
			elif ct == "image/png":
				flag = True
				allure.attach(body=response.content, name="png图片", attachment_type=allure.attachment_type.PNG)
			elif ct == "application/pdf":
				flag = True
				allure.attach(body=response.content, name="pdf", attachment_type=allure.attachment_type.PDF)
			if flag:
				path.parent.parent.joinpath('data').mkdir(parents=True, exist_ok=True)
				file = Path(path.parent.parent, 'data', (str(int(time.time())) + ".%s") % ct.split("/")[1])
				file.open(mode="wb").write(response.content)
				logger.info(f"{ct.split('/')[1]}格式文件下载成功，文件下载路径:{file}")
		return response
	return wapper


def logFixture(func):
	""" 日志记录 """
	def wapper(method, url, files=None, name=None, **kwargs):
		logger.info(f"{'接口请求开始':-^20}")
		logger.info(f"请求名称:{name}")
		logger.info(f"请求url:{url}")
		logger.info(f"请求方法:{method}")
		logger.info(f"请求参数:{kwargs}")
		logger.info(f"文件上传:{files}")
		response = func(method, url, files, **kwargs)
		logger.info(f"{'接口请求结束':-^20}")
		return response
	return wapper


def allureFixture(func):
	""" allure记录 """
	def wapper(method, url, files=None, **kwargs):
		allure.attach(body=url, name="请求url:", attachment_type=allure.attachment_type.TEXT)
		allure.attach(body=method, name="请求方式:", attachment_type=allure.attachment_type.TEXT)
		allure.attach(body=json.dumps(kwargs, ensure_ascii=False), name="请求参数:",
					  attachment_type=allure.attachment_type.TEXT)
		if files:
			allure.attach(body=json.dumps(files, ensure_ascii=False), name="文件上传:",
						  attachment_type=allure.attachment_type.TEXT)
		response = func(method, url, files, **kwargs)
		allure.attach(body=str(response.status_code), name="响应状态码:", attachment_type=allure.attachment_type.TEXT)
		data = None
		try:
			data = json.dumps(response.json(), ensure_ascii=False)
		except Exception:
			response.encoding = "utf-8"
			data = response.text
		finally:
			allure.attach(body=data, name="响应数据:", attachment_type=allure.attachment_type.TEXT)
		return response
	return wapper


@parameterHandle
@downloadFixture
@allureFixture
@logFixture
def send_request(method, url, files=None, **kwargs):
	""" 发送同一个session请求 """
	response = session.request(method=method, url=url, files=files, timeout=10, **kwargs)
	return response


def equalFrame(target, string):
	""" 相等断言 """
	for i, j in target.items():
		if j:
			if i == "status_code":  # 响应状态断言
				logger.info(f"预期结果状态码:{j}")
				logger.info(f"实际结果状态码:{string.status_code}")
				logger.info(f"相等断言:断言{'通过' if j == string.status_code else '失败'}")
				assert j == string.status_code, f"断言失败，预期结果状态码{j}不等于实际结果状态码{string.status_code}"
			else:  # 响应状态断言
				results = jsonpath.jsonpath(string.json(), "$..%s" % i)
				if results:
					if isinstance(j, str):  # 结果是个字符串
						for x in results:
							logger.info(f"预期结果:{j}")
							logger.info(f"实际结果:{x}")
							logger.info(f"相等断言:断言{'通过' if x == j else '失败'}")
							assert x == j, f"断言失败，预期结果{j}不等于实际结果{x}"
					elif isinstance(j, list):  # 结果是个列表
						logger.info(f"预期结果:{j}")
						logger.info(f"实际结果:{results}")
						seq = list(map(lambda a, b: True if a == b else False, j, results))
						assert all(seq), f"断言失败，预期结果{j}不等于实际结果{results}"
						logger.info(f"相等断言:断言{'通过' if all(seq) else '失败'}")
					else:
						raise Exception(f"validata中{i}只能是字符串或列表") from None
				else:
					raise Exception(f"在响应中未找到{i}") from None


def containFrame(target, string):
	""" 包含断言 """
	temp = ""
	try:
		data: dict = string.json()
		temp: str = json.dumps(data, ensure_ascii=False)
	except Exception:
		string.encoding = "utf-8"
		data: str = string.text
		temp: str = data
	finally:
		if target:
			seq = []
			for x in target:
				assert temp.find(x) != -1, f"断言失败，响应结果中未找到{x}"
				message = f"{x + '找到，断言通过' if temp.find(x) != -1 else x + '未找到，断言失败'}"
				seq.append(message)
			logger.info("包含断言:" + ",".join(seq))
