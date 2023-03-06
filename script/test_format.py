import allure
from common.read.readTestcase import readTestcase
from common.request.autoRequest import autoRequest
from functools import partial
from script.conftest import parametrize


@allure.epic("ddddpytest接口自动化测试项目")
@allure.feature("测试返回格式")
class TestHttpbin:

	rt = partial(readTestcase,"format.yaml")

	@allure.story("返回html")
	@parametrize(rt())
	async def test_html(self,case):
		allure.dynamic.title(case["casename"])
		return await autoRequest(case)

	@allure.story("返回png图片")
	@parametrize(rt(1))
	async def test_png(self,case):
		allure.dynamic.title(case["casename"])
		return await autoRequest(case)

	@allure.story("返回jpeg图片")
	@parametrize(rt(2))
	async def test_jpeg(self,case):
		allure.dynamic.title(case["casename"])
		return await autoRequest(case)