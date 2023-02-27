import requests
from common.request.fixture import *
from common.session.sessionManager import session


@allureFixture
@logFixture
@fileFixture
def request(method, url, files=None, sess=None, timeout=10, **kwargs) -> requests.Response:
	""" 发送请求 """
	return session(seek=sess).request(method=method, url=url, files=files, timeout=timeout, **kwargs)
