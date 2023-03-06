import allure
from common.read.readTestcase import readTestcase
from common.request.autoRequest import autoRequest
from script.conftest import parametrize


@allure.epic("ddddpytest接口自动化测试项目")
@allure.feature("测试data")
class TestHttpbin:

	@parametrize(readTestcase("data.yaml"))
	@allure.story("测试data")
	async def test_data(self,case):
		allure.dynamic.title(case["casename"])
		return await autoRequest(case)