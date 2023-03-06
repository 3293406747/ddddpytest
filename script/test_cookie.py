import allure
from common.read.readTestcase import readTestcase
from common.request.autoRequest import autoRequest
from functools import partial
from script.conftest import parametrize


@allure.epic("ddddpytest接口自动化测试项目")
@allure.feature("测试cookie")
class TestHttpbin:
	rt = partial(readTestcase, "cookie.yaml")

	@allure.story("session0获取cookie_1")
	@parametrize(rt())
	async def test_cookie0(self, case):
		allure.dynamic.title(case["casename"])
		return await autoRequest(case)

	@allure.story("session1获取cookie")
	@parametrize(rt(1))
	async def test_cookie1(self,case):
		allure.dynamic.title(case["casename"])
		return await autoRequest(case)

	@allure.story("session获取cookie_2")
	@parametrize(rt(2))
	async def test_cookie2(self,case):
		allure.dynamic.title(case["casename"])
		return await autoRequest(case)
