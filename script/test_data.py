import allure
import pytest
from common.read.readTestcase import readTestcase
from common.request.autoRequest import autoRequest


@allure.epic("ddddpytest接口自动化测试项目")
@allure.feature("测试data")
class TestHttpbin:

	@allure.story("测试data")
	@pytest.mark.parametrize("case", readTestcase("data.yaml"))
	def test_data(self, case):
		allure.dynamic.title(case["casename"])
		autoRequest(case)