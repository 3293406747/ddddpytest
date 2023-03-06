import asyncio
import pytest
from common.read.readTestcase import readTestcase
from common.request.autoRequest import autoRequest
from common.session.sessionManager import asyncSession

loop = asyncio.new_event_loop()
tasks = []


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
	loop.run_until_complete(asyncio.gather(*tasks))
	loop.run_until_complete(close_session())


def parametrize(params=None):
	def asyncio_append_to_tasks(func):
		def wapper(*args, **kwargs):
			if params:
				[tasks.append(loop.create_task(func(*args, param, **kwargs))) for param in params]
			else:
				tasks.append(loop.create_task(func(*args, **kwargs)))

		return wapper

	return asyncio_append_to_tasks
