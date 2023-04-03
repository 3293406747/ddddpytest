import functools
import json
from utils.logger import logger
import asyncio


def logWriter(asyncio_request):
	""" 日志记录 """

	lock = asyncio.Lock()

	@functools.wraps(asyncio_request)
	async def wrapper(method, url, sessionIndex: int = 0, **kwargs):
		response_content, response_content_type = await asyncio_request(method, url, sessionIndex, **kwargs)

		async with lock:
			logger.info(f"请求url:{url:.255s}")
			logger.info(f"请求方式:{method}")
			logger.info(f"请求参数:{json.dumps(kwargs, ensure_ascii=False):.255s}")
			content_type_maps = {
				"application/json": lambda: json.dumps(response_content, ensure_ascii=False),
				"text/html": response_content,
				"text/plain": response_content
			}

			if not response_content_type:
				logger.info("响应结果:响应结果headers中无Content-Type")
				return response_content,response_content_type

			if response_content_type in content_type_maps:
				if callable(content_type_maps[response_content_type]):
					response_content_str = content_type_maps[response_content_type]()
				else:
					response_content_str = content_type_maps[response_content_type]
				logger.info(f"响应结果:{response_content_str:.255s}")
			else:
				logger.info(f"响应结果:响应结果格式 {response_content_type} 暂不支持")

			return response_content,response_content_type

	return wrapper

# def allureFixture(func):
# 	""" allure记录 """
#
# 	lock = asyncio.Lock()
#
# 	@functools.wraps(func)
# 	async def wrapper(method, url, sess=0, **kwargs):
# 		response = await func(method=method, url=url, sess=sess, **kwargs)
#
# 		async with lock:
# 			allure.attach(url, "请求url", allure.attachment_type.TEXT)
# 			allure.attach(method, "请求方式", allure.attachment_type.TEXT)
# 			allure.attach(json.dumps(kwargs, ensure_ascii=False), "请求参数", allure.attachment_type.JSON)
# 			content_type_maps = {
# 				"image/jpeg": allure.attachment_type.JPG,
# 				"image/png": allure.attachment_type.PNG,
# 				"application/pdf": allure.attachment_type.PDF,
# 				"application/json": allure.attachment_type.JSON,
# 				"text/html": allure.attachment_type.HTML,
# 				"text/plain": allure.attachment_type.TEXT,
# 				"video/mp4": allure.attachment_type.MP4,
# 				"application/xml": allure.attachment_type.XML
# 			}
#
# 			response_content_type = response[1]
# 			if not response_content_type:
# 				allure.attach("响应结果:响应结果headers中无Content-Type", "响应数据", allure.attachment_type.TEXT)
# 				return response
#
# 			if response_content_type in content_type_maps:
# 				data = response[0]
# 				body = data if not isinstance(data, dict) else json.dumps(data, ensure_ascii=False)
# 				allure.attach(body, response_content_type, content_type_maps[response_content_type])
# 			else:
# 				allure.attach(f"响应结果格式 {response_content_type} 暂不支持", "响应数据", allure.attachment_type.TEXT)
# 			return response
#
# 	return wrapper
