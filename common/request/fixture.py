import functools
import json
import allure
from utils.logger import logger


def logFixture(func):
	""" 日志记录 """

	@functools.wraps(func)
	def wrapper(url, name, files=None, sess=None, timeout=10, method=None, **kwargs):
		logger.info(f"请求名称:{name:.255s}")
		logger.info(f"请求url:{url:.255s}")
		logger.info(f"请求方式:{method}")
		logger.info(f"请求参数:{json.dumps(kwargs, ensure_ascii=False):.255s}")

		response = func(url=url, files=files, sess=sess, timeout=timeout, method=method, **kwargs)

		logger.info(f"响应状态码:{str(response.status_code)}")

		content_type_maps = {
			"application/json": lambda: json.dumps(response.json(), ensure_ascii=False),
			"text/html": lambda: response.text,
			"text/plain": lambda: response.text
		}
		response_content_type = response.headers.get("Content-Type")
		if not response_content_type:
			logger.info("响应结果:响应结果headers中无Content-Type")
			return response

		response_content_type = response_content_type.split(";")[0].strip()
		if response_content_type in content_type_maps:
			logger.info(f"响应结果:{content_type_maps[response_content_type]():.255s}")
		else:
			logger.info(f"响应结果:响应结果格式 {response_content_type} 暂不支持")

		return response

	return wrapper


def allureFixture(func):
	""" allure记录 """

	@functools.wraps(func)
	def wrapper(url, sess=None, method=None, files=None, timeout=10, **kwargs):
		allure.attach(url, "请求url", allure.attachment_type.TEXT)
		allure.attach(method, "请求方式", allure.attachment_type.TEXT)
		allure.attach(json.dumps(kwargs, ensure_ascii=False), "请求参数", allure.attachment_type.JSON)

		response = func(method=method, url=url, sess=sess, files=files, timeout=timeout, **kwargs)

		allure.attach(str(response.status_code), "响应状态码", allure.attachment_type.TEXT)

		content_type_maps = {
			"image/jpeg": allure.attachment_type.JPG,
			"image/png": allure.attachment_type.PNG,
			"application/pdf": allure.attachment_type.PDF,
			"application/json": allure.attachment_type.JSON,
			"text/html": allure.attachment_type.HTML,
			"text/plain": allure.attachment_type.TEXT,
			"video/mp4": allure.attachment_type.MP4,
			"application/xml": allure.attachment_type.XML
		}

		response_content_type = response.headers.get("Content-Type")
		if not response_content_type:
			allure.attach("响应结果:响应结果headers中无Content-Type", "响应数据", allure.attachment_type.TEXT)
			return response

		response_content_type = response_content_type.split(";")[0].strip()
		if response_content_type in content_type_maps:
			allure.attach(response.content, response_content_type, content_type_maps[response_content_type])
		else:
			allure.attach(f"响应结果格式 {response_content_type} 暂不支持", "响应数据", allure.attachment_type.TEXT)
		return response

	return wrapper
