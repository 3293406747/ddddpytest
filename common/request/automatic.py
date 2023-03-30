import copy
import json
from functools import partial
from pathlib import Path
from common.case.renderTemplate import render_template
from common.request.fixture import logWriter
from common.session.manager import asyncSession
from utils.assertion import Assertion
from utils.extract import Extract
from utils.variablesManager import variables, environments


async def autoRequest(test_case: dict) -> dict:
	""" 自动请求 """
	# 合并变量池
	merged_variables_pool = {**variables.pool, **environments.pool}

	# 渲染请求
	rendered_request = render_template(test_case["request"], merged_variables_pool)

	# 获取用例名称、请求url、请求方法、session index
	name = test_case["casename"]
	url = rendered_request.pop("url")
	method = rendered_request.pop("method")
	sessionIndex = test_case.get("session", 0)

	# 发送请求
	response, response_content_type = await asyncio_request(method, url, sessionIndex, **rendered_request)

	# 格式化响应结果和请求参数为字符串
	request_formatted = format_request(rendered_request)
	response_formatted = format_response(response, response_content_type)

	# 提取内容
	extracted_variables_pool = extract(test_case, response_formatted)

	# 合并变量池
	merged_variables_pool = {**merged_variables_pool, **extracted_variables_pool}

	# 断言
	assert_result = assertion(test_case, response_formatted, merged_variables_pool)

	# 组装结果
	result = {
		"用例名称": name,
		"请求url": url,
		"请求方法": method,
		"请求参数": request_formatted,
		"响应结果类型": response_content_type,
		"响应结果": response_formatted,
		"断言": assert_result
	}

	return result


def format_request(request: str | dict):
	"""格式化请求参数为字符串"""
	if isinstance(request, str):
		return request
	elif isinstance(request, dict):
		return json.dumps(request, ensure_ascii=False)
	else:
		return "请求参数类型不支持"


def format_response(response: str | dict, response_content_type: str):
	"""格式化响应结果为字符串"""
	if response_content_type in ["text/html", "text/plain"]:
		return response
	elif response_content_type == "application/json":
		return json.dumps(response, ensure_ascii=False)
	else:
		return "响应结果类型不支持"


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


def assertion(test_case: dict, http_response: str, mapping: dict) -> list:
	""" 断言 """
	assertions = []
	assertions_config = test_case.get("assertion")
	if assertions_config is None:
		return assertions

	methods = {"equal": Assertion.equal, "unequal": Assertion.unequal, "contain": Assertion.contian,
			   "uncontain": Assertion.uncontian}
	# 使用提取的内容和变量池进行渲染
	assertions_config = render_template(assertions_config, mapping)
	# 不懂啊 不知道为何有时候json.loads后还是str
	assertions_config = json.loads(assertions_config) if isinstance(assertions_config, str) else assertions_config

	for assertion_method, assertion_results in assertions_config.items():
		assertion_group = {"method": assertion_method, "value": []}
		for assertion_result in assertion_results:
			expected, actual_value = assertion_result.get("expect"), assertion_result.get("actual")
			expected = expected.split(",") if isinstance(expected, str) else expected
			if actual_value == "response":
				if http_response != "响应结果类型不支持":
					actual_value = http_response
				else:
					raise TypeError("响应结果类型不支持")
			elif assertion_method in ["equal", "unequal"]:
				actual_value = actual_value.split(",") if isinstance(actual_value, str) else actual_value
			msg = methods[assertion_method](expected, actual_value)
			assertion_group["value"].append({"expect": expected, "actual": actual_value, "result": msg})
		assertions.append(assertion_group)
	return assertions


def read_files(input_files: dict) -> None:
	"""读取文件"""
	project_root = Path(__file__).resolve().parent.parent.parent
	if not isinstance(input_files, dict):
		raise TypeError("参数 input_files 必须为字典类型")
	for file_name, file_path in input_files.items():
		if not isinstance(file_path, str):
			raise TypeError("参数 file_path 必须为字符串类型")
		file_abs_path = project_root / file_path
		if not file_abs_path.exists():
			raise FileNotFoundError(f"指定文件 {file_abs_path} 不存在")
		with open(file_abs_path, "rb") as f:
			file_content = f.read()
		input_files[file_name] = file_content


# @allureFixture
# @logFixture
# def request(method, url, files=None, sess=None, timeout=10, name=None, **kwargs) -> requests.Response:
# 	""" 发送请求 """
# 	return session(seek=sess).request(method=method, url=url, files=files, timeout=timeout, **kwargs)

@logWriter
async def asyncio_request(method: str, url: str, session_index: int = 0, **kwargs) -> tuple:
	"""发送异步请求"""
	request_params = copy.deepcopy(kwargs)

	# 文件处理
	files = request_params.pop("files", None)
	if files:
		read_files(files)
		request_params["data"] = files

	async with asyncSession.get_session(session_index).request(method=method, url=url, **request_params) as response:
		content_type = response.headers.get("Content-Type")
		if content_type is None:
			result = await response.text()
			return result, content_type

		content_type = content_type.split(";")[0].strip()
		if content_type in ["text/html", "text/plain"]:
			result = await response.text()
		elif content_type == "application/json":
			result = await response.json()
		else:
			result = await response.read()
		return result, content_type
