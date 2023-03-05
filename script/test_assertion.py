import allure
import pytest
from common.read.readTestcase import readTestcase
from common.request.autoRequest import autoRequest
from functools import partial
from script.conftest import asyncio_append_to_tasks


@allure.epic("ddddpytest接口自动化测试项目")
@allure.feature("测试assertion")
class TestHttpbin:

	rt = partial(readTestcase,"assertion.yaml")

	@allure.story("相等断言")
	@asyncio_append_to_tasks(rt())
	@pytest.mark.parametrize("case", rt())
	async def test_equalassertion(self,case):
		allure.dynamic.title(case["casename"])
		await autoRequest(case)

	@allure.story("包含断言")
	@asyncio_append_to_tasks(rt(1))
	@pytest.mark.parametrize("case", rt(1))
	async def test_containassertion(self,case):
		allure.dynamic.title(case["casename"])
		await autoRequest(case)


	@allure.story("数据库断言")
	@asyncio_append_to_tasks(rt(2))
	@pytest.mark.parametrize("case", rt(2))
	async def test_sqlassertion(self,case):
		allure.dynamic.title(case["casename"])
		await autoRequest(case)