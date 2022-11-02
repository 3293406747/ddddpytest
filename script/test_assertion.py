import allure
import pytest
from common import dp


@allure.epic("ddddpytest接口自动化测试项目")
@allure.feature("测试assertion")
class TestHttpbin:

	@allure.story("断言")
	@pytest.mark.parametrize("case", dp.read_testcase("assertion.yaml"))
	def test_assertion(self, case):
		allure.dynamic.title(case.pop("casename"))
		dp.requests().autoRequest(**case.get("request"),extract=case.get("extract"),assertion_=case.get("assertion"))


	@allure.story("数据库断言")
	@pytest.mark.parametrize("case", dp.read_testcase("assertion.yaml",1))
	def test_sqlassertion(self, case):
		allure.dynamic.title(case.pop("casename"))
		dp.requests().autoRequest(**case.get("request"),extract=case.get("extract"),assertion_=case.get("assertion"))