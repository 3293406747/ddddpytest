import copy
import json
from functools import partial
from pathlib import Path
from common.case.renderTemplate import renderTemplate
from common.request.fixture import logWriter
from common.session.manager import asyncSession
from utils.assertion import Assertion
from utils.extract import Extract
from utils.variablesManager import variables, environments


async def autoRequest(caseinfo: dict):
	""" 自动请求 """
	# 合并变量池
	variablesPoolByMerge = {**variables.pool, **environments.pool}
	# 渲染请求
	request = caseinfo["request"]
	request = renderTemplate(request, variablesPoolByMerge)
	# 获取用例名称
	name = caseinfo["casename"]
	# 请求url
	url = request.pop("url")
	# 请求方法
	method = request.pop("method")
	# 获取session index
	sessionIndex = caseinfo.get("session", 0)
	# 发送请求
	result = await asyncioRequest(method, url, sessionIndex, **request)
	# 从请求或响应中提取内容:
	response = result[0]
	extractPool = extract(caseinfo, response)
	# 字符串格式响应结果
	response_content_type = result[1]
	if response_content_type in ["text/html", "text/plain"]:
		response = response
	elif response_content_type == "application/json":
		response = json.dumps(response, ensure_ascii=False)
	else:
		response = "响应结果类型不支持"
	# 字符串格式请求参数
	if isinstance(request, str):
		request = request
	elif isinstance(request, dict):
		request = json.dumps(request, ensure_ascii=False)
	else:
		request = "请求参数类型不支持"
	# 合并变量池
	variablesPoolByMerge = {**variablesPoolByMerge, **extractPool}
	# 断言
	assert_result = assertion(caseinfo, response, variablesPoolByMerge)

	result = {
		"用例名称": name,
		"请求url": url,
		"请求方法": method,
		"请求参数": request,
		"响应结果类型": response_content_type,
		"响应结果": response,
		"断言": assert_result
	}

	return result


def extract(test_case: dict, http_response: str) -> dict:
	""" 从请求或响应中提取内容 """
	extracted_data = {}
	if test_case.get("extract") is None:
		return extracted_data

	for data_type, extract_config in test_case["extract"].items():
		data_source = test_case["request"] if data_type == "request" else http_response
		for extracted_key, extract_pattern in extract_config.items():
			extract_parts = str(extract_pattern).split(",")
			extract_pattern = extract_parts[0]
			extract_index = int(extract_parts[1]) if len(extract_parts) > 1 else None
			extract_func = partial(Extract.json if extract_pattern.startswith("$") else Extract.match)
			extracted_value = extract_func(data_source, extract_pattern, extract_index)
			extracted_data[extracted_key] = extracted_value
	return extracted_data


def assertion(caseinfo, response, mapping):
	""" 断言 """
	assertion_map = []
	assertions = caseinfo.get("assertion")
	if not assertions:
		return assertion_map

	# 使用提取的内容和变量池进行渲染
	data = renderTemplate(assertions, mapping)
	# 不懂啊 不知道为何有时候json.loads后还是str
	data = json.loads(data) if isinstance(data, str) else data

	for method, value in data.items():
		tmpPool = {"method": method, "value": []}

		methods = {
			"equal": Assertion.equal,
			"unequal": Assertion.unequal,
			"contain": Assertion.contian,
			"uncontain": Assertion.uncontian
		}
		for item in value:
			expect, actual = item.get("expect"), item.get("actual")
			if isinstance(expect, str):
				expect = expect.split(",")
			if actual == "response":
				if response != "响应结果类型不支持":
					actual = response
				else:
					raise TypeError("响应结果类型不支持")
			elif method in ["equal", "unequal"]:
				if isinstance(actual, str):
					actual = actual.split(",")
			msg = methods[method](expect, actual)

			tmpPool["value"].append({"expect": expect, "actual": actual, "result": msg})
		assertion_map.append(tmpPool)

	return assertion_map


def read_files(files: dict) -> None:
	"""文件处理"""
	project_dir = Path(__file__).resolve().parent.parent.parent
	if not isinstance(files, dict):
		raise TypeError("参数 files 必须为字典类型")
	for file, path in files.items():
		if not isinstance(path, str):
			raise TypeError("参数 path 必须为字符串类型")
		file_path = project_dir / path
		if not Path(file_path).exists():
			raise FileNotFoundError(f"指定文件 {file_path} 不存在")
		with open(file_path, "rb") as f:
			files[file] = f.read()


# @allureFixture
# @logFixture
# def request(method, url, files=None, sess=None, timeout=10, name=None, **kwargs) -> requests.Response:
# 	""" 发送请求 """
# 	return session(seek=sess).request(method=method, url=url, files=files, timeout=timeout, **kwargs)

@logWriter
async def asyncioRequest(method, url, sessionIndex=0, **kwargs):
	params = copy.deepcopy(kwargs)

	# 文件处理
	files = params.pop("files", None)
	if files:
		read_files(files)
		params["data"] = files

	async with asyncSession.get_session(sessionIndex).request(method=method, url=url, **params) as response:
		content_type = response.headers.get("Content-Type")
		if not content_type:
			result = await response.text()
			content_type = None
			return result, content_type

		content_type = content_type.split(";")[0].strip()
		if content_type in ["text/html", "text/plain"]:
			result = await response.text()
		elif content_type == "application/json":
			result = await response.json()
		else:
			result = await response.read()
		return result, content_type
