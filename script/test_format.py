import allure
import pytest
from common.read.readTestcase import readTestcase
from common.request.autoRequest import autoRequest
from functools import partial


@allure.epic("ddddpytest接口自动化测试项目")
@allure.feature("测试返回格式")
class TestHttpbin:

	rt = partial(readTestcase,"format.yaml")

	@allure.story("返回html")
	@pytest.mark.parametrize("case", rt())
	def test_html(self, case):
		allure.dynamic.title(case["casename"])
		autoRequest(case)

	@allure.story("返回png图片")
	@pytest.mark.parametrize("case", rt(1))
	def test_png(self, case):
		allure.dynamic.title(case["casename"])
		autoRequest(case)

	@allure.story("返回jpeg图片")
	@pytest.mark.parametrize("case", rt(2))
	def test_jpeg(self, case):
		allure.dynamic.title(case["casename"])
		autoRequest(case)