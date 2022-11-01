import pytest
from common import dp


@pytest.fixture(scope="session",autouse=True,params=dp.read_testcase("setcookie.yaml"))
def prelogin(request):
	dp.requests().get(**request.param.get("request"))
	dp.session().create()


