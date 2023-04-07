from common.read.case import read_case
from debug import auto_request
from debug.script.conftest import parametrize


# @allure.epic("ddddpytest接口自动化测试项目")
# @allure.feature("测试data")
class TestHttpbin:

	@parametrize(read_case("debug/testcase/data.yaml"))
	# @allure.story("测试data")
	async def test_data(self,case):
		# allure.dynamic.title(case["casename"])
		return await auto_request(case)