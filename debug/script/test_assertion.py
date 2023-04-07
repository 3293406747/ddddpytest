from common.read.case import read_case
from debug import auto_request
from functools import partial
from debug.script.conftest import parametrize


# @allure.epic("ddddpytest接口自动化测试项目")
# @allure.feature("测试assertion")
class TestHttpbin:

	rt = partial(read_case, "debug/testcase/assertion.yaml")

	@parametrize(rt())
	# @allure.story("相等断言")
	async def test_equalassertion(self,case):
		# allure.dynamic.title(case["casename"])
		return await auto_request(case)

	@parametrize(rt(1))
	# @allure.story("包含断言")
	async def test_containassertion(self,case):
		# allure.dynamic.title(case["casename"])
		return await auto_request(case)


	@parametrize(rt(2))
	# @allure.story("数据库断言")
	async def test_sqlassertion(self,case):
		# allure.dynamic.title(case["casename"])
		return await auto_request(case)