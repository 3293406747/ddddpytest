import allure
import pytest
from common.read.readTestcase import readTestcase
from common.request.autoRequest import autoRequest
from functools import partial


@allure.epic("ddddpytest接口自动化测试项目")
@allure.feature("测试assertion")
class TestHttpbin:

	rt = partial(readTestcase,"assertion.yaml")

	@allure.story("相等断言")
	@pytest.mark.parametrize("case", rt())
	def test_equalassertion(self, case):
		allure.dynamic.title(case["casename"])
		autoRequest(case)

	@allure.story("包含断言")
	@pytest.mark.parametrize("case", rt(1))
	def test_containassertion(self, case):
		allure.dynamic.title(case["casename"])
		autoRequest(case)


	@allure.story("数据库断言")
	@pytest.mark.parametrize("case", rt(2))
	def test_sqlassertion(self, case):
		allure.dynamic.title(case["casename"])
		autoRequest(case)