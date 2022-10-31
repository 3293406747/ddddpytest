import allure
import pytest
from common import dp


@allure.epic("ddddpytest接口自动化测试项目")		# 项目名称
@allure.feature("httpbin接口自动化测试")			# 模块名称
class TestHttpbin:

	@allure.severity(allure.severity_level.CRITICAL)		# 优先级 可以修饰方法，也可以修饰类
	@allure.link(url="http://httpbin.org",name="接口文档地址")
	@allure.story("get接口")			# 接口名称
	@pytest.mark.parametrize("data",dp.read_case("test1.csv"))		# 读取用例文件
	def test_getapi(self, data):
		# allure.dynamic.title(testcase["name"])		# 用例名称
		allure.dynamic.description("无")			# 用例描述
		base_url = dp.variables().get('base_url')
		url = base_url + "/post"
		method = "POST"
		dp.variables().set("value", "123456")
		data = dp.case_parse(data)
		response = dp.requests().request(method=method, url=url, data=data)
		value = response.extractVariable().json('$..value', 0)
		dp.asserion().equal("123456", value, "相等断言")

	# @allure.story("post接口")		# 接口名称
	# @allure.link(url="https://httpbin.org",name="接口文档地址")
	# @pytest.mark.parametrize("testcase", read_testcase("PostApi.yaml"))
	# def test_postapi(self, testcase):
	# 	allure.dynamic.title(testcase["name"])
	# 	allure.dynamic.description("无")
	# 	autoSendRequest(testcase)
