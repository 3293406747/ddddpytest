import asyncio
import time

import pytest
from common.read.readTestcase import readTestcase
from common.reporter.reporter import ExcelReport
from common.request.autoRequest import autoRequest
from common.session.sessionManager import asyncSession
from pathlib import Path

loop = asyncio.new_event_loop()
tasks = []
REPORTS_DIR = Path(__file__).parent.parent.joinpath("reports").resolve()


@pytest.fixture(scope='session', autouse=True)
def event_loop():
	yield loop
	loop.close()


@pytest.fixture(scope='session', autouse=True, params=readTestcase("setcookie.yaml"))
def session(request):
	async def close_session():
		await asyncSession.close()

	async def setup(case):
		asyncSession.create_session()  # 创建session
		asyncSession.create_session()
		await autoRequest(case)  # 设置cookie

	loop.run_until_complete(setup(request.param))
	yield
	data_map = loop.run_until_complete(asyncio.gather(*tasks))
	loop.run_until_complete(close_session())
	# 生成报告
	path = REPORTS_DIR.joinpath(time.strftime('%Y-%m-%d'))
	path.mkdir(parents=True, exist_ok=True)
	report = ExcelReport(path.joinpath(f"report_{time.strftime('%H_%M_%S')}.xlsx"))
	for data in data_map:
		report.write_to_container(data)
	report.save()


def parametrize(params=None):
	def asyncio_append_to_tasks(func):
		def wapper(*args, **kwargs):
			if params:
				[tasks.append(loop.create_task(func(*args, param, **kwargs))) for param in params]
			else:
				tasks.append(loop.create_task(func(*args, **kwargs)))

		return wapper

	return asyncio_append_to_tasks
