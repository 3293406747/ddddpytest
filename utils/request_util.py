import json
import os
import re
import time
import jsonpath
import pytest
import requests
import yaml
from utils.logger_util import logger
from utils.yaml_util import read_extract, write_extract
from mako.template import Template


__all__ = ["auto_send_request", "send_request", "extract_variable"]

base_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
data_path = os.path.join(base_path,"data")
session = requests.session()


def render_template(data):
	""" 渲染用例 """
	data = json.dumps(data) if data and isinstance(data,dict) else data
	extract = read_extract()
	# extract.yaml文件可能为空，为空时不渲染用例
	if extract and data:
		temp = Template(data).render(**extract)
		response = yaml.load(stream=temp, Loader=yaml.FullLoader)
		return response
	else:
		return None

def send_request(method,url,base_url=None,caseinfo=None,start=None,**kwargs):
	""" 发送同一个session请求 """
	method = str(method).lower()
	new_url = render_template(url)
	# 未经过渲染时使用原来的url，未渲染会导致url变为None
	url = new_url if new_url else url
	for key,value in kwargs.items():
		if key in ("headers","params","data","json"):
			new_value = render_template(value)
			kwargs[key] = new_value if new_value else value
	# 配置中无base_url或者send_request方法不传入base_url参数，都会使base_url为None
	if base_url:
		url = base_url + url
	else:
		url = url
	logger.info(f"{'接口请求开始':-^20}")
	if caseinfo:
		logger.info(f"请求名称:{caseinfo['name']}")
	logger.info(f"请求url:{url}")
	logger.info(f"请求方法:{method}")
	logger.info(f"请求参数:{kwargs}")
	response = session.request(method=method,url=url,**kwargs)
	type_ = ["image/jpeg", "image/png", "application/pdf"]
	download(response,type_)
	if caseinfo:
		extract_variable(response, caseinfo, start=start)
		new_validata = render_template(caseinfo["validata"])
		caseinfo["validata"] = new_validata if new_validata else caseinfo["validata"]
		assertion(caseinfo,response)
		logger.info(f"{'接口请求结束':-^20}\n")
	return response

def auto_send_request(caseinfo,start=None):
	""" 获取用例自动发送请求 """
	url = caseinfo["request"].pop("url")
	method = caseinfo["request"].pop("method")
	base_url = caseinfo["base_url"]
	if caseinfo["request"].get("files"):
		for key,value in dict(caseinfo["request"]["files"]).items():
			dict(caseinfo["request"]["files"])[key] = open(value,"rb")
	response = send_request(method=method,url=url,base_url=base_url,caseinfo=caseinfo,start=start,**caseinfo["request"])
	return response

def extract_variable(string,case_info,start=None):
	""" 接口关联:提取响应中的内容 """
	if "extract" in case_info.keys():
		for key,value in case_info["extract"].items():
			tf_list = list(map(lambda x : True if x in value else False,["$",">","(",")"]))
			if all(tf_list):
				# json+正则提取器
				json_extract,re_extract = str(string.json()).split(">")
				temp = jsonpath.jsonpath(str(json_extract).strip(), value)[0]
				response = re.search(str(re_extract).strip(), temp).group(1)
			elif "(" in value and ")" in value:
				# 正则提取器
				response = re.search(value,string.text).group(1)
			elif "$" in value:
				# json提取器
				response = jsonpath.jsonpath(string.json(),value)[0]
			else:
				raise Exception("提取器表达式错误") from None
			if start:
				response = start + response
			target = {key: response}
			write_extract(target)

def assertion(caseinfo,string):
	""" 响应断言 """
	validata = caseinfo["validata"]
	if isinstance(validata,dict):
		for key,value in validata.items():
			if key == "equal":
				# 相等断言
				if isinstance(value,dict):
					for i,j in value.items():
						if i == "status_code":
							# 响应状态断言
							logger.info(f"预期结果状态码:{j}")
							logger.info(f"实际结果状态码:{string.status_code}")
							logger.info(f"相等断言:断言{'通过' if j == string.status_code else '失败'}")
							assert j == string.status_code, f"断言失败，预期结果状态码{j}不等于实际结果状态码{string.status_code}"
						else:
							# 响应结果断言
							results = jsonpath.jsonpath(string.json(),"$..%s"%i)
							if results:
								if isinstance(j,str):
									# 结果是个字符串
									for x in results:
										logger.info(f"预期结果:{j}")
										logger.info(f"实际结果:{x}")
										logger.info(f"相等断言:断言{'通过' if x == j else '失败'}")
										assert x == j,f"断言失败，预期结果{j}不等于实际结果{x}"
								elif isinstance(j,list):
									# 结果是个列表
									logger.info(f"预期结果:{j}")
									logger.info(f"实际结果:{results}")
									seq = list(map(lambda a,b: True if a == b else False,j,results))
									assert all(seq),f"断言失败，预期结果{j}不等于实际结果{results}"
									logger.info(f"相等断言:断言{'通过' if all(seq) else '失败'}")
								else:
									raise Exception(f"validata中{i}只能是字符串或列表") from None
							else:
								raise Exception(f"在响应中未找到{i}") from None
			elif key == "contain":
				try:
					data = string.json()
					if isinstance(data,dict):
						temp = json.dumps(data,ensure_ascii=False)
				except TypeError:
					string.encoding = "utf-8"
					data = string.text
					if isinstance(data,str):
						temp = data
				finally:
					seq = []
					for x in validata["contain"]:
						assert temp.find(x) != -1,f"断言失败，响应结果中未找到{x}"
						message = f"{x+'找到，断言通过' if temp.find(x) != -1 else x+'未找到，断言失败'}"
						seq.append(message)
					logger.info("包含断言:"+",".join(seq))

def download(response,target):
	""" 文件下载 """
	if response.headers.get("Content-Type"):
		tp = target.pop()
		if tp in response.headers["Content-Type"]:
			if not os.path.exists(data_path):
				os.mkdir(data_path)
			file = os.path.join(data_path,str(int(time.time()))+".%s") % tp.split("/")[1]
			with open(file=file,mode="wb") as f:
				f.write(response.content)
				logger.info(f"{tp.split('/')[1]}格式文件下载成功，文件下载路径:{file}")
			return None
		elif not target:
			return None
		else:
			return download(response,target)

