import json
from functools import partial

from common.case.render_template import render_template
from common.request.fixture import logWriter, handle_files
from common.session.manager import asyncSession
from utils.assert_data import assert_data
from utils.extract_data import Extract
from utils.logger_manager import logger
from utils.variables_manager import variables, environments


async def auto_request(case: dict) -> dict:
	""" 自动请求 """
	# 合并变量池
	merged_variables_pool = {**variables.pool, **environments.pool}

	# 渲染请求
	rendered_request = render_template(case["request"], merged_variables_pool)

	# 获取用例名称、请求url、请求方法、session index
	name = case["casename"]
	url = rendered_request.pop("url")
	method = rendered_request.pop("method")
	sessionIndex = case.get("session", 0)

	# 发送请求
	response, response_content_type = await asyncio_request(method, url, sessionIndex, **rendered_request)

	# 格式化响应结果和请求参数为字符串
	request_formatted = _format_request(rendered_request)
	response_formatted = _format_response(response, response_content_type)

	# 提取内容
	extracted_variables_pool = _extract(case, response_formatted)

	# 合并变量池
	merged_variables_pool = {**merged_variables_pool, **extracted_variables_pool}

	# 断言
	assert_result = _assert(case, response_formatted, merged_variables_pool)

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


def _format_request(request: str | dict):
	"""格式化请求参数为字符串"""
	if isinstance(request, str):
		return request
	elif isinstance(request, dict):
		return json.dumps(request, ensure_ascii=False)
	else:
		return "请求参数类型不支持"


def _format_response(response: str | dict, response_content_type: str):
	"""格式化响应结果为字符串"""
	if response_content_type in ["text/html", "text/plain"]:
		return response
	elif response_content_type == "application/json":
		return json.dumps(response, ensure_ascii=False)
	else:
		return "响应结果类型不支持"


def _extract(case: dict, http_response: str) -> dict:
	""" 从请求或响应中提取内容 """
	extracted_data = {}
	if case.get("extract") is None:
		return extracted_data

	for data_type, extract_config in case["extract"].items():
		data_source = case["request"] if data_type == "request" else http_response
		for extracted_key, extract_pattern in extract_config.items():
			extract_parts = str(extract_pattern).split(",")
			extract_pattern = extract_parts[0]
			extract_index = int(extract_parts[1]) if len(extract_parts) > 1 else None
			extract_func = partial(Extract.json if extract_pattern.startswith("$") else Extract.match)
			extracted_value = extract_func(data_source, extract_pattern, extract_index)
			extracted_data[extracted_key] = extracted_value
	return extracted_data


def _assert(case: dict, http_response: str, mapping: dict) -> list:
	""" 断言 """
	assertions = []
	assertions_config = case.get("assertion")
	if assertions_config is None:
		return assertions

	methods = {"equal": assert_data.equal, "unequal": assert_data.unequal, "contain": assert_data.contian,
			   "uncontain": assert_data.uncontian}
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
				# 与用户输入无关的程序内部错误可以使用assert而不是raise
				assert http_response != "响应结果类型不支持", "响应结果类型不支持"
				actual_value = http_response
			elif assertion_method in ["equal", "unequal"]:
				actual_value = actual_value.split(",") if isinstance(actual_value, str) else actual_value
			msg = methods[assertion_method](expected, actual_value)
			assertion_group["value"].append({"expect": expected, "actual": actual_value, "result": msg})
		assertions.append(assertion_group)
	return assertions


# 尽量不使用装饰器 难定位分析bug
@logWriter(logger)
@handle_files
async def asyncio_request(method: str, url: str, session_index: int = 0, **kwargs) -> tuple:
	"""发送异步请求"""
	async with asyncSession.get_session(session_index).request(method=method, url=url, **kwargs) as response:
		response_content_type = response.headers.get("Content-Type")
		if response_content_type is None:
			response_content = await response.text()
			return response_content, response_content_type

		response_content_type = response_content_type.split(";")[0].strip()
		if response_content_type in ["text/html", "text/plain"]:
			response_content = await response.text()
		elif response_content_type == "application/json":
			response_content = await response.json()
		else:
			response_content = await response.read()
		return response_content, response_content_type

# @allureFixture
# @logFixture
# def request(method, url, files=None, sess=None, timeout=10, name=None, **kwargs) -> requests.Response:
# 	""" 发送请求 """
# 	return session(seek=sess).request(method=method, url=url, files=files, timeout=timeout, **kwargs)
