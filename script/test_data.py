from common.read.testcase import read_case
from common.request.automatic import auto_request
from script.conftest import parametrize


# @allure.epic("ddddpytest接口自动化测试项目")
# @allure.feature("测试data")
class TestHttpbin:

	@parametrize(read_case("data.yaml"))
	# @allure.story("测试data")
	async def test_data(self,case):
		# allure.dynamic.title(case["casename"])
		return await auto_request(case)