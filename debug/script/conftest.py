import asyncio
import time

from pathlib import Path
import pytest

from common.read.config import read_config
from common.read.case import read_case
from common.reporter.reporter import ExcelReport
from debug import auto_request
from common.session.manager import asyncSession
from utils.send_email import send_email, SendEmailConfig

# 避免使用全局变量
LOOP = asyncio.new_event_loop()
REPORTS_DIR = Path(__file__).resolve().parent.parent.joinpath("reports").joinpath(time.strftime('%Y-%m-%d'))
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
_tasks = []
_report_path: Path
_error_log_path: Path


async def _setup(case):
	asyncSession.create_session()  # 创建session
	asyncSession.create_session()
	await auto_request(case)  # 设置cookie


@pytest.fixture(scope='package', autouse=True)
def event_loop():
	yield LOOP
	LOOP.close()


async def _close_session():
	await asyncSession.close_all_session()


@pytest.fixture(scope='package', autouse=True, params=read_case("debug/testcase/setcookie.yaml"))
def session(request):
	LOOP.run_until_complete(_setup(request.param))
	yield
	data_map = LOOP.run_until_complete(asyncio.gather(*_tasks))
	LOOP.run_until_complete(_close_session())
	# 生成报告
	global _report_path
	_report_path = REPORTS_DIR.joinpath(f"report_{time.strftime('%H_%M_%S')}.xlsx")
	report = ExcelReport()
	try:
		for data in data_map:
			report.write_to_container(data)
	finally:
		report.pre_save()
		report.save(_report_path)
		report.close()
		print("测试报告已生成,路径:\n", _report_path)
		if report.failed_number != 0:
			raise AssertionError("测试用例执行未全部通过")


def parametrize(params=None):
	def asyncio_append_to_tasks(func):
		def wapper(*args, **kwargs):
			if params:
				[_tasks.append(LOOP.create_task(func(*args, param, **kwargs))) for param in params]
			else:
				_tasks.append(LOOP.create_task(func(*args, **kwargs)))

		return wapper

	return asyncio_append_to_tasks


# pytest hook
def pytest_exception_interact(node, call, report):
	if report.failed:
		exc_info = call.excinfo
		global _error_log_path
		_error_log_path = REPORTS_DIR.joinpath(f"error_log_{time.strftime('%H_%M_%S')}.log")
		with open(_error_log_path, 'w') as f:
			f.write(f'测试用例执行异常\n')
			f.write(f'报错位置: {node.nodeid}\n')
			f.write(f"概要信息: {str(exc_info.getrepr(style='normal'))}\n")
			f.write(f"详细信息:\n {str(exc_info.getrepr(style='short'))}\n")
			f.write(f"完整报错信息:\n {str(exc_info.getrepr('long'))}")
			f.write('=' * 20 + '\n')


# pytest hook
def pytest_terminal_summary(terminalreporter):
	email_config = read_config("debug/config/local.yaml")["email"]
	if not email_config["flag"]:
		return

	filename_list = []
	if 'error' in terminalreporter.stats:
		# 构造文本内容
		text = email_config.pop("failed_text")
		email_config.pop("success_text")

		if str(_report_path):
			filename_list.append(_report_path)
		filename_list.append(_error_log_path)
	else:
		# 构造文本内容
		text = email_config.pop("success_text")
		email_config.pop("failed_text")

		filename_list.append(_report_path)

	# 发送邮件
	config = SendEmailConfig(text=text, filename_list=filename_list, **email_config)
	send_email(config)
