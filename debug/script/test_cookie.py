from common.read.case import read_case
from debug import auto_request
from functools import partial
from debug.script.conftest import parametrize


# @allure.epic("ddddpytest接口自动化测试项目")
# @allure.feature("测试cookie")
class TestHttpbin:
	rt = partial(read_case, "debug/testcase/cookie.yaml")

	@parametrize(rt())
	# @allure.story("session0获取cookie_1")
	async def test_cookie0(self, case):
		# allure.dynamic.title(case["casename"])
		return await auto_request(case)

	@parametrize(rt(1))
	# @allure.story("session1获取cookie")
	async def test_cookie1(self,case):
		# allure.dynamic.title(case["casename"])
		return await auto_request(case)

	@parametrize(rt(2))
	# @allure.story("session获取cookie_2")
	async def test_cookie2(self,case):
		# allure.dynamic.title(case["casename"])
		return await auto_request(case)
