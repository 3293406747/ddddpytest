import functools
import json
from json import JSONDecodeError
import allure
from utils.logger import logger
from pathlib import Path


class fixture:

	@classmethod
	def logfixture(cls, func):
		""" 日志记录 """

		@functools.wraps(func)
		def wrapper(url, name, files=None, sess=None, timeout=10, method=None, **kwargs):
			logger.info(f"请求名称:{name:.255s}")
			logger.info(f"请求url:{url:.255s}")
			if method:
				logger.info(f"请求方式:{method}")
			logger.info(f"请求参数:{json.dumps(kwargs, ensure_ascii=False):.255s}")
			if files:
				logger.info(f"文件上传:{json.dumps(files, ensure_ascii=False):.255s}")
			real = func(url=url, files=files, sess=sess, timeout=timeout, method=method, **kwargs)
			try:
				data = json.dumps(real.json(), ensure_ascii=False)
			except JSONDecodeError:
				data = real.text
			logger.info(f"响应结果:{data:.255s}")
			return real

		return wrapper

	@classmethod
	def files(cls, func):
		""" 文件处理 """

		@functools.wraps(func)
		def wrapper(url, sess=None, method=None, files=None, timeout=10, **kwargs):
			if isinstance(files, dict):
				for file, path in files.items():
					project_path = Path(__file__).resolve().parent.parent.parent
					path = project_path / path
					files[file] = open(path, "rb")
			real = func(url=url, sess=sess, method=method, files=files, timeout=timeout, **kwargs)
			return real

		return wrapper

	@classmethod
	def allure(cls, func):
		""" allure记录 """

		@functools.wraps(func)
		def wrapper(url, sess=None, method=None, files=None, timeout=10, **kwargs):
			allure.attach(body=url, name="请求url:", attachment_type=allure.attachment_type.TEXT)
			if method:
				allure.attach(body=method, name="请求方式:", attachment_type=allure.attachment_type.TEXT)
			allure.attach(body=json.dumps(kwargs, ensure_ascii=False), name="请求参数:",
						  attachment_type=allure.attachment_type.TEXT)
			if files:
				allure.attach(body=json.dumps(files, ensure_ascii=False), name="文件上传:",
							  attachment_type=allure.attachment_type.TEXT)
			response = func(method=method, url=url, sess=sess, files=files, timeout=timeout, **kwargs)
			allure.attach(body=str(response.status_code), name="响应状态码:", attachment_type=allure.attachment_type.TEXT)
			try:
				data = json.dumps(response.json(), ensure_ascii=False)
			except JSONDecodeError:
				data = response.text
			allure.attach(body=data, name="响应数据:", attachment_type=allure.attachment_type.TEXT)
			if isinstance(response.content, bytes) and response.headers.get("Content-Type"):
				ct = response.headers["Content-Type"]
				if ct == "image/jpeg":
					allure.attach(body=response.content, name="image", attachment_type=allure.attachment_type.JPG)
				elif ct == "image/png":
					allure.attach(body=response.content, name="image", attachment_type=allure.attachment_type.PNG)
				elif ct == "application/pdf":
					allure.attach(body=response.content, name="pdf", attachment_type=allure.attachment_type.PDF)
			return response

		return wrapper