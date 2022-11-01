import base64
import hashlib
from common.mock import Mock
from common.mysql import SqlSelect


def md5(string):
	""" md5加密 """
	if not isinstance(string,str):
		raise TypeError('string must be a string')
	encode = string.encode()
	return hashlib.md5(encode).hexdigest()

def bearer(string):
	""" base64加密 """
	if not isinstance(string,str):
		raise TypeError('string must be a string')
	return base64.b64encode(string.encode()).decode()

def mock():
	""" 生成mock数据 """
	return Mock()

def sqlSelect(sql,key,item=None):
	""" sql查询 """
	return SqlSelect().execute(sql=sql,key=key,item=int(item))