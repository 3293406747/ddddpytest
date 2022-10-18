import pytest
from common.request import autoSendRequest
from common.template import login


@pytest.fixture(scope="session",autouse=True)
def prelogin():
	value = login()
	if value:
		autoSendRequest(value)


