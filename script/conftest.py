import pytest
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


