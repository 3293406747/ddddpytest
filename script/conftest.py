import pytest
from common.request import autoSendRequest
from common.yaml import read_testcase, read_config


@pytest.fixture(scope="session",autouse=True)
def login():
	login = read_config("login")
	if isinstance(login,int):
		caseinfo = read_testcase("login.yaml")[read_config("login")]
		autoSendRequest(caseinfo)
	elif not login:
		pass
	else:
		raise TypeError("login must be a int")


