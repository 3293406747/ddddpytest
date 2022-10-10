""" 模块已废弃 """
import base64

def basic_auth(user,passwd):
	""" 示例代码中处理base64加密鉴权的方法 """
	auth = "Basic " + base64.b64encode(":".join([user,passwd]).encode()).decode()
	return auth