import copy
import json
from functools import partial
from pathlib import Path
from common.case.renderTemplate import renderTemplate
from common.request.fixture import logFixture
from common.session.sessionManager import asyncSession
from utils.assertion import Assertion
from utils.extract import Extract
from utils.variablesManager import variables, environments


async def autoRequest(caseinfo):
	""" 自动请求 """
	# 合并变量池
	mapping = {**variables.pool, **environments.pool}
	# 渲染请求
	caseinfo["request"] = renderTemplate(caseinfo["request"], mapping)
	# 获取用例名称
	name = caseinfo["casename"]
	request = caseinfo["request"]
	# 请求url
	url = request.pop("url")
	# 请求方法
	method = request.pop("method")
	# 获取session index
	sess = caseinfo.get("session", 0)
	# 发送请求
	response = await asyncioRequest(method=method, url=url, **caseinfo["request"], sess=sess)
	# 从请求或响应中提取内容:
	extractPool = getExtracts(caseinfo, response[0])

	if response[1] in ["text/html", "text/plain"]:
		response_result = response[0]
	elif response[1] == "application/json":
		response_result = json.dumps(response[0], ensure_ascii=False)
	else:
		response_result = "响应结果类型不支持"

	# 合并变量池
	mapping = {**mapping, **extractPool}
	# 断言
	assert_result = assertion(caseinfo, response_result, mapping)

	request_params = caseinfo["request"]
	if isinstance(request_params, str):
		request_params = request_params
	elif isinstance(request_params, dict):
		request_params = json.dumps(request_params, ensure_ascii=False)
	else:
		request_params = "请求参数类型不支持"

	result = {
		"用例名称": name,
		"请求url": url,
		"请求方法": method,
		"请求参数": request_params,
		"响应结果类型": response[1],
		"响应结果": response_result,
		"断言": assert_result
	}

	return result


def getExtracts(caseinfo, response) -> dict:
	""" 提取内容 """
	extractPool = {}
	if caseinfo.get("extract") is None:
		return extractPool

	data = response

	for method, value in caseinfo["extract"].items():
		data = caseinfo["request"] if method == "request" else data
		for key, pattern in value.items():
			pattern_parts = str(pattern).split(",")
			pattern = pattern_parts[0]
			index = int(pattern_parts[1]) if len(pattern_parts) > 1 else None
			extract_fn = partial(Extract.json if pattern.startswith("$") else Extract.match)
			value = extract_fn(data, pattern, index)
			extractPool[key] = value

	return extractPool


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
			if isinstance(expect,str):
				expect = expect.split(",")
			if actual == "response":
				if response != "响应结果类型不支持":
					actual = response
				else:
					raise TypeError("响应结果类型不支持")
			elif method in ["equal", "unequal"]:
				if isinstance(actual,str):
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

@logFixture
async def asyncioRequest(method, url, sess=0, **kwargs):
	params = copy.deepcopy(kwargs)

	# 文件处理
	files = params.pop("files", None)
	if files:
		read_files(files)
		params["data"] = files

	async with asyncSession.get_session(sess).request(method=method, url=url, **params) as response:
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
