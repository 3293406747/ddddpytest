import allure
import pytest
from common import dp


@allure.epic("ddddpytest接口自动化测试项目")		# 项目名称
@allure.feature("httpbin接口自动化测试")			# 模块名称
class TestHttpbin:

	@allure.severity(allure.severity_level.CRITICAL)		# 优先级 可以修饰方法，也可以修饰类
	@allure.link(url="http://httpbin.org",name="接口文档地址")
	@allure.story("get接口")			# 接口名称
	@pytest.mark.parametrize("case", dp.read_testcase("test1.yaml"))		# 读取用例文件
	def test_getapi(self, case):
		allure.dynamic.title(case.pop("name"))		# 用例名称
		allure.dynamic.description("无")			# 用例描述

		dp.variables().set("value", "123456")

		response = dp.requests().autoRequest(**case)
		value = response.extractVariable().json('$..value', 0)
		dp.asserion().equal("123456", value, "相等断言")

	# @allure.story("post接口")		# 接口名称
	# @allure.link(url="https://httpbin.org",name="接口文档地址")
	# @pytest.mark.parametrize("testcase", read_testcase("PostApi.yaml"))
	# def test_postapi(self, testcase):
	# 	allure.dynamic.title(testcase["name"])
	# 	allure.dynamic.description("无")
	# 	autoSendRequest(testcase)
