import time

import pytest
from common.logger import logger
from common.read import read_config
from common.variable import Variables
from common import dp


@pytest.fixture(scope="session",autouse=True,params=dp.read_testcase("setcookie.yaml"))
def prelogin(request):
	# 设置base_url为变量
	Variables().set(key="base_url", value=read_config()["base_url"])
	# 创建session
	dp.session().new()
	# 设置cookie
	dp.autoRequest(request.param)
	# 创建session
	dp.session().new()


@pytest.fixture(autouse=True)
def caselog_start_end():
	start_time = time.time()
	logger.info(f"{'测试用例开始执行':*^60s}")
	yield
	logger.info(f"{'测试用例执行结束':*^60s}")
	end_time = time.time()
	logger.info(f"测试用例执行耗时：{end_time - start_time:.3f}秒")



