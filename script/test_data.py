import allure
import pytest
from common import dp


@allure.epic("ddddpytest接口自动化测试项目")
@allure.feature("测试data")
class TestHttpbin:

	@allure.story("测试data")
	@pytest.mark.parametrize("case", dp.read_testcase("data.yaml"))
	def test_data(self, case):
		allure.dynamic.title(case["casename"])
		dp.autoRequest(case)