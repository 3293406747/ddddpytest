import pytest
from utils.request_util import auto_send_request
from utils.yaml_util import read_testcase

# 读取用例文件
@pytest.mark.parametrize("testcase",read_testcase("httpbin.yaml"))
def test_demo(testcase):
	# 自动发送请求，接口关联，断言
	auto_send_request(testcase)