import allure
import pytest
from common.read.readTestcase import readTestcase
from common.request.autoRequest import autoRequest
from functools import partial
from script.conftest import asyncio_append_to_tasks


@allure.epic("ddddpytest接口自动化测试项目")
@allure.feature("测试返回格式")
class TestHttpbin:

	rt = partial(readTestcase,"format.yaml")

	@allure.story("返回html")
	@asyncio_append_to_tasks(rt())
	@pytest.mark.parametrize("case", rt())
	async def test_html(self,case):
		allure.dynamic.title(case["casename"])
		await autoRequest(case)

	@allure.story("返回png图片")
	@asyncio_append_to_tasks(rt(1))
	@pytest.mark.parametrize("case", rt(1))
	async def test_png(self,case):
		allure.dynamic.title(case["casename"])
		await autoRequest(case)

	@allure.story("返回jpeg图片")
	@asyncio_append_to_tasks(rt(2))
	@pytest.mark.parametrize("case", rt(2))
	async def test_jpeg(self,case):
		allure.dynamic.title(case["casename"])
		await autoRequest(case)