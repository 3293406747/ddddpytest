import time
import pytest
from common.read.readConfig import readConfig
from common.read.readTestcase import readTestcase
from common.request.autoRequest import autoRequest
from common.session.sessionManager import session
from utils.logger import logger
from utils.variablesManager import variables


@pytest.fixture(scope="session",autouse=True,params=readTestcase("setcookie.yaml"))
def setup_login(request):
	variables.set(key="base_url", value=readConfig()["base_url"])		# 设置base_url为变量
	session.new()														# 创建session
	autoRequest(request.param)											# 设置cookie
	session.new()														# 创建session


@pytest.fixture(autouse=True)
def case_timer():
	start_time = time.time()
	logger.info(f"{'测试用例开始执行':*^60s}")
	yield
	logger.info(f"{'测试用例执行结束':*^60s}")
	end_time = time.time()
	logger.info(f"测试用例执行耗时：{end_time - start_time:.3f}秒")



