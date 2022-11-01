import allure
import pytest
from common import dp
from common.mysql import SqlSelect


@allure.epic("ddddpytest接口自动化测试项目")
@allure.feature("测试assertion")
class TestHttpbin:

	@allure.story("断言")
	@pytest.mark.parametrize("case", dp.read_testcase("assertion.yaml"))
	def test_assertion(self, case):
		allure.dynamic.title(case.pop("casename"))
		response = dp.requests().autoRequest(**case.get("request"))
		extract = response.extractVariable().json("$..foo",0)
		dp.asserion().equal(expect=case["assertion"]["foo"],actual=extract)


	@allure.story("数据库断言")
	@pytest.mark.parametrize("case", dp.read_testcase("assertion.yaml",1))
	def test_sqlassertion(self, case):
		allure.dynamic.title(case.pop("casename"))
		response = dp.requests().autoRequest(**case.get("request"))
		extract = response.extractVariable().json("$..foo", 0)
		SqlSelect().commit(f"INSERT INTO `user` VALUES ('{extract}', '女', 21, '15803456513', '211204196204245151', '375370181699897', DEFAULT, DEFAULT)")
		expect = dp.useFunc(case["assertion"]["foo"])
		dp.asserion().equal(expect=expect, actual=extract)