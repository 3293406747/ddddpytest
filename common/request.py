import json
import re
import time
import allure
import jsonpath
import requests
import yaml
from common.logger import logger
from common.mysql import RegexSql
from common.assertion import AssertionFactory
from mako.template import Template
from pathlib import Path

__all__ = ["autoSendRequest", "send_request", "extract_variable"]

path = Path(__file__).resolve()
session = requests.session()
extractPool = {}

def sqlSelect(func):
	def wapper(caseinfo):
		response = func(caseinfo)
		if not caseinfo['validata'] or not isinstance(caseinfo['validata'],dict):
			return response
		for sqls in caseinfo['validata'].values():
			if isinstance(sqls,list):
				for n,sql in enumerate(sqls):
					if isinstance(sql, str) and re.search('%.*?%', sql):
						sqls[n] = re.sub(r'%(.*?)%',RegexSql().select,sql)
			elif isinstance(sqls,dict):
				for key,sql in sqls.items():
					if isinstance(sql,str) and re.search('%.*?%',sql):
						sqls[key] = re.sub(r'%(.*?)%',RegexSql().select,sql)
		return response
	return wapper

def extract_variable(func):
	""" 接口关联:提取响应中的内容 """
	def wapper(caseinfo):
		response = func(caseinfo)
		if "extract" in caseinfo.keys():
			for key, value in caseinfo["extract"].items():
				if "(" in value and ")" in value:  # 正则提取器
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
		if not isinstance(caseinfo["validata"], dict):
			return response
		for k,v in caseinfo["validata"].items():
			x,y = str(k).split("|")
			at = AssertionFactory(x)
			if isinstance(v,list):
				for pattern in v:
					temp = at.create(pattern,response,index=0)
					match y:
						case 'exist':
							temp.exist()
						case 'unexist':
							temp.unexist()
						case _:
							raise ValueError
			elif isinstance(v,dict):
				for pattern,expect in v.items():
					temp = at.create(pattern,response,index=0)
					match y:
						case 'equal':
							temp.equal(expect)
						case 'unequal':
							temp.unequal(expect)
						case _:
							raise ValueError
		return response
	return wapper


@assertion
@sqlSelect
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
