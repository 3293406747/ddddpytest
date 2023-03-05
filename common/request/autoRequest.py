import json
from pathlib import Path
from string import Template
import aiohttp
from common.case.renderTemplate import renderTemplate
from common.request.fixture import allureFixture, logFixture
from common.session.sessionManager import asyncSession
from utils.extract import Extract
from utils.assertion import Assertion
from functools import partial


async def autoRequest(caseinfo):
	""" 自动请求 """
	# 渲染请求
	caseinfo["request"] = renderTemplate(caseinfo["request"])
	# 获取session
	sess = caseinfo.get("session", 0)
	# 获取用例名称
	name = caseinfo["casename"]
	# 文件处理
	files = caseinfo["request"].get("files")
	if files:
		read_files(files)
	# 发送请求
	response = await asyncioRequest(**caseinfo["request"], sess=sess, files=files)
	# # 从请求或响应中提取内容:
	extractPool = getExtracts(caseinfo, response[0])
	# 断言
	assertion(caseinfo, response[0], extractPool)
	return response


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


def assertion(caseinfo, response, extractPool):
	""" 断言 """
	assertions = caseinfo.get("assertion")
	if not assertions:
		return

	# 使用从请求中提取的内容进行渲染
	temp = Template(json.dumps(assertions, ensure_ascii=False)).safe_substitute(extractPool)
	data = renderTemplate(temp)
	# 不懂啊 不知道为何有时候json.loads后还是str
	data = json.loads(data) if isinstance(data, str) else data

	for method, value in data.items():
		# 相等或不相等断言
		if method in ["equal", "unequal"]:
			assert_fn = partial(Assertion.equal if method == "equal" else Assertion.unequal)
			for item in value:
				expect, actual, name = item.get("expect"), item.get("actual"), item.get("name")
				expect, actual = expect.split(","), actual.split(",")
				assert_fn(expect, actual, name)
		# 包含或不包含断言
		elif method in ["contain", "uncontain"]:
			assert_fn = partial(Assertion.contian if method == "contain" else Assertion.uncontian)
			actual = response

			for expect in value:
				expect = expect.split(",")
				assert_fn(expect, actual)


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
async def asyncioRequest(method, url, files=None, sess=0, **kwargs):
	async with asyncSession.get_session(sess).request(method=method, url=url, **kwargs) as response:
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
