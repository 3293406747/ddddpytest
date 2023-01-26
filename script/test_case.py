import allure
import pytest
from common.read.readTestcase import readTestcase
from common.request.autoRequest import autoRequest
from utils.variables import variables


@allure.epic("ddddpytest接口自动化测试项目")
@allure.feature("测试case")
class TestHttpbin:

	@allure.story("使用内置变量")
	@pytest.mark.parametrize("case", readTestcase("case.yaml"))
	def test_innervariable(self, case):
		allure.dynamic.title(case["casename"])
		autoRequest(case)

	@allure.story("使用自定义变量")
	@pytest.mark.parametrize("case", readTestcase("case.yaml",1))
	def test_variable(self, case):
		allure.dynamic.title(case["casename"])
		variables.set("variable","variable_value")
		autoRequest(case)

	@allure.story("使用自定义全局变量")
	@pytest.mark.parametrize("case", readTestcase("case.yaml",2))
	def test_global(self, case):
		allure.dynamic.title(case["casename"])
		autoRequest(case)

	@allure.story("使用自定义环境变量")
	@pytest.mark.parametrize("case", readTestcase("case.yaml",3))
	def test_envirenment(self, case):
		allure.dynamic.title(case["casename"])
		autoRequest(case)

	@allure.story("调用python函数")
	@pytest.mark.parametrize("case", readTestcase("case.yaml",4))
	def test_python(self, case):
		allure.dynamic.title(case["casename"])
		autoRequest(case)