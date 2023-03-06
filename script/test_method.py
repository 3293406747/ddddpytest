import allure
from common.read.readTestcase import readTestcase
from common.request.autoRequest import autoRequest
from functools import partial
from script.conftest import parametrize


# 优先级 可以修饰方法，也可以修饰类
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(url="http://httpbin.org", name="接口文档地址")
# 项目名称
@allure.epic("ddddpytest接口自动化测试项目")
# 模块名称
@allure.feature("测试method")
class TestHttpbin:

	rt = partial(readTestcase,"method.yaml")

	# 接口名称
	@allure.story("get请求")
	# 读取用例文件
	@parametrize(rt())
	async def test_get(self,case):
		# 用例名称
		allure.dynamic.title(case["casename"])
		# 发送请求
		return await autoRequest(case)

	@allure.story("post请求data传参")
	@parametrize(rt(1))
	async def test_postdata(self,case):
		allure.dynamic.title(case["casename"])
		return await autoRequest(case)

	@allure.story("post请求json传参")
	@parametrize(rt(2))
	async def test_postjson(self,case):
		allure.dynamic.title(case["casename"])
		return await autoRequest(case)

	@allure.story("post请求文件上传")
	@parametrize(rt(3))
	async def test_postfiles(self,case):
		allure.dynamic.title(case["casename"])
		return await autoRequest(case)
