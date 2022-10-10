import allure
import pytest
from common.request import autoSendRequest
from common.yaml import read_testcase


@allure.epic("ddddpytest接口自动化测试项目")		# 项目名称
@allure.feature("httpbin接口自动化测试")			# 模块名称
class TestHttpbin:

	@allure.severity(allure.severity_level.CRITICAL)		# 优先级 可以修饰方法，也可以修饰类
	@allure.link(url="http://httpbin.org",name="接口文档地址")
	@allure.story("get接口")			# 接口名称
	@pytest.mark.parametrize("testcase",read_testcase("GetApi.yaml"))		# 读取用例文件
	def test_getapi(self, testcase):
		allure.dynamic.title(testcase["name"])		# 用例名称
		allure.dynamic.description("无")			# 用例描述
		autoSendRequest(testcase)					# 发送请求、接口关联、断言、热加载、下载文件

	@allure.story("post接口")		# 接口名称
	@allure.link(url="https://httpbin.org",name="接口文档地址")
	@pytest.mark.parametrize("testcase", read_testcase("PostApi.yaml"))
	def test_postapi(self, testcase):
		allure.dynamic.title(testcase["name"])
		allure.dynamic.description("无")
		autoSendRequest(testcase)
