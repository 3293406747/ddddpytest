import pytest
from common import dp


@pytest.fixture(scope="session",autouse=True,params=dp.read_testcase("setcookie.yaml"))
def prelogin(request):
	dp.requests().autoRequest(request.param)
	dp.session().create()


