import time
import pytest
from common.read.readConfig import readConfig
from common.read.readTestcase import readTestcase
from common.request.autoRequest import autoRequest
from common.session.session import session
from utils.logger import logger
from utils.variables import variables


@pytest.fixture(scope="session",autouse=True,params=readTestcase("setcookie.yaml"))
def prelogin(request):
	# 设置base_url为变量
	variables.set(key="base_url", value=readConfig()["base_url"])
	# 创建session
	session.new()
	# 设置cookie
	autoRequest(request.param)
	# 创建session
	session.new()


@pytest.fixture(autouse=True)
def caselog_start_end():
	start_time = time.time()
	logger.info(f"{'测试用例开始执行':*^60s}")
	yield
	logger.info(f"{'测试用例执行结束':*^60s}")
	end_time = time.time()
	logger.info(f"测试用例执行耗时：{end_time - start_time:.3f}秒")



