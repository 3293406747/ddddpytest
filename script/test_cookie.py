import allure
import pytest
from common.read.readTestcase import readTestcase
from common.request.autoRequest import autoRequest
from functools import partial
from script.conftest import asyncio_append_to_tasks


@allure.epic("ddddpytest接口自动化测试项目")
@allure.feature("测试cookie")
class TestHttpbin:
	rt = partial(readTestcase, "cookie.yaml")

	@allure.story("session0获取cookie_1")
	@asyncio_append_to_tasks(rt())
	@pytest.mark.parametrize("case", rt())
	async def test_cookie0(self, case):
		allure.dynamic.title(case["casename"])
		return await autoRequest(case)

	@allure.story("session1获取cookie")
	@asyncio_append_to_tasks(rt(1))
	@pytest.mark.parametrize("case", rt(1))
	async def test_cookie1(self,case):
		allure.dynamic.title(case["casename"])
		return await autoRequest(case)

	@allure.story("session获取cookie_2")
	@asyncio_append_to_tasks(rt(2))
	@pytest.mark.parametrize("case", rt(2))
	async def test_cookie2(self,case):
		allure.dynamic.title(case["casename"])
		return await autoRequest(case)
