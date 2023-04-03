import asyncio
import time
import pytest
from common.read.config import readConfig
from common.read.testcase import readTestcase
from common.reporter.reporter import ExcelReport
from utils.sendEmail import send_email
from common.request.automatic import autoRequest
from common.session.manager import asyncSession
from pathlib import Path

loop = asyncio.new_event_loop()
tasks = []
REPORTS_DIR = Path(__file__).parent.parent.joinpath("reports").joinpath(time.strftime('%Y-%m-%d')).resolve()
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
REPORT_PATH = None
ERROR_LOG_PATH = None


@pytest.fixture(scope='session', autouse=True)
def event_loop():
	yield loop
	loop.close()


@pytest.fixture(scope='session', autouse=True, params=readTestcase("setcookie.yaml"))
def session(request):
	async def close_session():
		await asyncSession.close_all_session()

	async def setup(case):
		asyncSession.create_session()  # 创建session
		asyncSession.create_session()
		await autoRequest(case)  # 设置cookie

	loop.run_until_complete(setup(request.param))
	yield
	data_map = loop.run_until_complete(asyncio.gather(*tasks))
	loop.run_until_complete(close_session())
	# 生成报告
	global REPORT_PATH
	REPORT_PATH = REPORTS_DIR.joinpath(f"report_{time.strftime('%H_%M_%S')}.xlsx")
	report = ExcelReport(REPORT_PATH)
	try:
		for data in data_map:
			report.write_to_container(data)
	finally:
		report.save()
		print("测试报告已生成,路径:\n", REPORT_PATH)
		if report.failed_number != 0:
			raise AssertionError("测试用例执行未全部通过")


def parametrize(params=None):
	def asyncio_append_to_tasks(func):
		def wapper(*args, **kwargs):
			if params:
				[tasks.append(loop.create_task(func(*args, param, **kwargs))) for param in params]
			else:
				tasks.append(loop.create_task(func(*args, **kwargs)))

		return wapper

	return asyncio_append_to_tasks


# pytest hook
def pytest_exception_interact(node, call, report):
	if report.failed:
		exc_info = call.excinfo
		global ERROR_LOG_PATH
		ERROR_LOG_PATH = REPORTS_DIR.joinpath(f"error_log_{time.strftime('%H_%M_%S')}.log")
		with open(ERROR_LOG_PATH, 'w') as f:
			f.write(f'测试用例执行异常\n')
			f.write(f'报错位置: {node.nodeid}\n')
			f.write(f"概要信息: {str(exc_info.getrepr(style='normal'))}\n")
			f.write(f"详细信息:\n {str(exc_info.getrepr(style='short'))}\n")
			f.write(f"完整报错信息:\n {str(exc_info.getrepr('long'))}")
			f.write('=' * 20 + '\n')


# pytest hook
def pytest_terminal_summary(terminalreporter):
	email_config = readConfig()["email"]
	if not email_config["flag"]:
		return

	filename_map = []
	if 'error' in terminalreporter.stats:
		# 构造文本内容
		text = email_config.pop("failed_text")
		email_config.pop("success_text")
		if str(REPORT_PATH):
			filename_map.append(REPORT_PATH)
		filename_map.append(ERROR_LOG_PATH)
	else:
		# 构造文本内容
		text = email_config.pop("success_text")
		email_config.pop("failed_text")
		filename_map.append(REPORT_PATH)
	send_email(text=text, filename_map=filename_map, **email_config)
