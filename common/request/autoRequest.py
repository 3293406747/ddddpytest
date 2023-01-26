import json,re
from json import JSONDecodeError
from string import Template
import requests
from common.case.render import renderTemplate
from utils.extract import extract
from common.request.request import request
from utils.assertion import Assertion


def autoRequest(caseinfo, timeout=10) -> requests.Response:
	""" 自动请求 """
	# 渲染请求
	caseinfo["request"] = renderTemplate(caseinfo["request"])
	# 获取session
	sess = caseinfo.get("session")
	# 获取用例名称
	name = caseinfo["casename"]
	# 发送请求
	response = request(**caseinfo["request"], name=name, sess=sess, timeout=timeout)
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
					value = extract.json(data=caseinfo["request"] if who == "request" else response.json(),
										 pattern=pattern, index=index)
				else:
					# 正则提取
					try:
						data = response.json()
					except JSONDecodeError:
						data = response.text
					value = extract.match(data=caseinfo["request"] if who == "request" else data, pattern=pattern,
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
						Assertion.equal(expect=expect, actual=actual, name=name)
					else:
						Assertion.unequal(expect=expect, actual=actual, name=name)
			# 包含或不包含断言
			elif method in ["contain", "uncontain"]:
				try:
					actual = response.json()
				except JSONDecodeError:
					actual = response.text
				for expect in value:
					expect = re.sub(r"\[?\s?'(.*?)'\]?", r"\1", expect).split(",")
					if method == "contain":
						Assertion.contian(expect=expect, actual=actual)
					else:
						Assertion.uncontian(expect=expect, actual=actual)
	return response
