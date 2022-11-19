import allure
import pytest
from common import dp


@allure.epic("ddddpytest接口自动化测试项目")
@allure.feature("测试返回格式")
class TestHttpbin:

	@allure.story("返回html")
	@pytest.mark.parametrize("case", dp.read_testcase("format.yaml"))
	def test_html(self, case):
		allure.dynamic.title(case["casename"])
		dp.autoRequest(case)

	@allure.story("返回png图片")
	@pytest.mark.parametrize("case", dp.read_testcase("format.yaml",1))
	def test_png(self, case):
		allure.dynamic.title(case["casename"])
		dp.autoRequest(case)

	@allure.story("返回jpeg图片")
	@pytest.mark.parametrize("case", dp.read_testcase("format.yaml",2))
	def test_jpeg(self, case):
		allure.dynamic.title(case["casename"])
		dp.autoRequest(case)