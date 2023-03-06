import allure
from common.read.readTestcase import readTestcase
from common.request.autoRequest import autoRequest
from functools import partial
from script.conftest import parametrize


@allure.epic("ddddpytest接口自动化测试项目")
@allure.feature("测试assertion")
class TestHttpbin:

	rt = partial(readTestcase,"assertion.yaml")

	@allure.story("相等断言")
	@parametrize(rt())
	async def test_equalassertion(self,case):
		allure.dynamic.title(case["casename"])
		return await autoRequest(case)

	@allure.story("包含断言")
	@parametrize(rt(1))
	async def test_containassertion(self,case):
		allure.dynamic.title(case["casename"])
		return await autoRequest(case)


	@allure.story("数据库断言")
	@parametrize(rt(2))
	async def test_sqlassertion(self,case):
		allure.dynamic.title(case["casename"])
		return await autoRequest(case)