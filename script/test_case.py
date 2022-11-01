import allure
import pytest
from common import dp


@allure.epic("ddddpytest接口自动化测试项目")
@allure.feature("测试case")
class TestHttpbin:

	@allure.story("使用内置变量")
	@pytest.mark.parametrize("case", dp.read_testcase("case.yaml"))
	def test_innervariable(self, case):
		allure.dynamic.title(case.pop("casename"))
		dp.requests().autoRequest(**case.get("request"))

	@allure.story("使用自定义变量")
	@pytest.mark.parametrize("case", dp.read_testcase("case.yaml",1))
	def test_variable(self, case):
		allure.dynamic.title(case.pop("casename"))
		dp.environment().set("variable","variable_value")
		dp.requests().autoRequest(**case.get("request"))

	@allure.story("使用自定义全局变量")
	@pytest.mark.parametrize("case", dp.read_testcase("case.yaml",2))
	def test_global(self, case):
		allure.dynamic.title(case.pop("casename"))
		dp.requests().autoRequest(**case.get("request"))

	@allure.story("使用自定义环境变量")
	@pytest.mark.parametrize("case", dp.read_testcase("case.yaml",3))
	def test_envirenment(self, case):
		allure.dynamic.title(case.pop("casename"))
		dp.requests().autoRequest(**case.get("request"))

	@allure.story("调用python函数")
	@pytest.mark.parametrize("case", dp.read_testcase("case.yaml",4))
	def test_python(self, case):
		allure.dynamic.title(case.pop("casename"))
		dp.requests().autoRequest(**case.get("request"))