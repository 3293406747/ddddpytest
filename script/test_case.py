import allure
import pytest
from common.read.readTestcase import readTestcase
from common.request.autoRequest import autoRequest
from script.conftest import asyncio_append_to_tasks
from utils.variablesManager import variables
from functools import partial


@allure.epic("ddddpytest接口自动化测试项目")
@allure.feature("测试case")
class TestHttpbin:

	rt = partial(readTestcase,"case.yaml")

	@allure.story("使用内置变量")
	@asyncio_append_to_tasks(rt())
	@pytest.mark.parametrize("case", rt())
	async def test_innervariable(self,case):
		allure.dynamic.title(case["casename"])
		return await autoRequest(case)

	@allure.story("使用自定义变量")
	@asyncio_append_to_tasks(rt(1))
	@pytest.mark.parametrize("case", rt(1))
	async def test_variable(self,case):
		allure.dynamic.title(case["casename"])
		variables.set("variable","variable_value")
		return await autoRequest(case)

	@allure.story("使用自定义环境变量")
	@asyncio_append_to_tasks
	@pytest.mark.parametrize("case", rt(2))
	async def test_envirenment(self,case):
		allure.dynamic.title(case["casename"])
		return await autoRequest(case)

	@allure.story("调用python函数")
	@asyncio_append_to_tasks
	@pytest.mark.parametrize("case", rt(3))
	async def test_python(self,case):
		allure.dynamic.title(case["casename"])
		return await autoRequest(readTestcase(case))