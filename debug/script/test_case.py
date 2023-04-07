from common.read.case import read_case
from debug import auto_request
from debug.script.conftest import parametrize
from debug import system_variables
from functools import partial


# @allure.epic("ddddpytest接口自动化测试项目")
# @allure.feature("测试case")
class TestHttpbin:

	rt = partial(read_case, "debug/testcase/case.yaml")

	@parametrize(rt())
	# @allure.story("使用内置变量")
	async def test_innervariable(self,case):
		# allure.dynamic.title(case["casename"])
		return await auto_request(case)

	@parametrize(rt(1))
	# @allure.story("使用自定义变量")
	async def test_variable(self,case):
		# allure.dynamic.title(case["casename"])
		system_variables.set("variable","variable_value")
		return await auto_request(case)

	@parametrize(rt(2))
	# @allure.story("使用自定义环境变量")
	async def test_envirenment(self,case):
		# allure.dynamic.title(case["casename"])
		return await auto_request(case)

	@parametrize(rt(3))
	# @allure.story("调用python函数")
	async def test_python(self,case):
		# allure.dynamic.title(case["casename"])
		return await auto_request(case)