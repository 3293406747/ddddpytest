import allure
import pytest
from common.read.readTestcase import readTestcase
from common.request.autoRequest import autoRequest

@allure.epic("ddddpytest接口自动化测试项目")
@allure.feature("测试cookie")
class TestHttpbin:

	@allure.story("session0获取cookie_1")
	@pytest.mark.parametrize("case", readTestcase("cookie.yaml"))
	def test_cookie0(self, case):
		allure.dynamic.title(case["casename"])
		autoRequest(case)

	@allure.story("session1获取cookie")
	@pytest.mark.parametrize("case", readTestcase("cookie.yaml",1))
	def test_cookie1(self, case):
		allure.dynamic.title(case["casename"])
		autoRequest(case)

	@allure.story("session获取cookie_2")
	@pytest.mark.parametrize("case", readTestcase("cookie.yaml",2))
	def test_cookie2(self, case):
		allure.dynamic.title(case["casename"])
		autoRequest(case)