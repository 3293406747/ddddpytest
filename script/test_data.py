import allure
import pytest
from common.read.readTestcase import readTestcase
from common.request.autoRequest import autoRequest
from script.conftest import asyncio_append_to_tasks


@allure.epic("ddddpytest接口自动化测试项目")
@allure.feature("测试data")
class TestHttpbin:

	@allure.story("测试data")
	@asyncio_append_to_tasks(readTestcase("data.yaml"))
	@pytest.mark.parametrize("case", readTestcase("data.yaml"))
	async def test_data(self,case):
		allure.dynamic.title(case["casename"])
		await autoRequest(case)