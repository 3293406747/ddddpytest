from common.read.case import read_case
from debug import auto_request
from functools import partial
from debug.script.conftest import parametrize


# # 优先级 可以修饰方法，也可以修饰类
# @allure.severity(allure.severity_level.CRITICAL)
# @allure.link(url="http://httpbin.org", name="接口文档地址")
# # 项目名称
# @allure.epic("ddddpytest接口自动化测试项目")
# # 模块名称
# @allure.feature("测试method")
class TestHttpbin:

	rt = partial(read_case, "debug/testcase/method.yaml")

	# 读取用例文件
	@parametrize(rt())
	# 接口名称
	# @allure.story("get请求")
	async def test_get(self,case):
		# # 用例名称
		# allure.dynamic.title(case["casename"])
		# 发送请求
		return await auto_request(case)

	@parametrize(rt(1))
	# @allure.story("post请求data传参")
	async def test_postdata(self,case):
		# allure.dynamic.title(case["casename"])
		return await auto_request(case)

	@parametrize(rt(2))
	# @allure.story("post请求json传参")
	async def test_postjson(self,case):
		# allure.dynamic.title(case["casename"])
		return await auto_request(case)

	@parametrize(rt(3))
	# @allure.story("post请求文件上传")
	async def test_postfiles(self,case):
		# allure.dynamic.title(case["casename"])
		return await auto_request(case)
