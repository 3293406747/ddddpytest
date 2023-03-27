import base64, hashlib, time
from utils.mock import Mock
from common.read.readMysql import readMysql
from functools import lru_cache


def md5(string: str) -> str:
	""" md5加密函数 """
	if not isinstance(string, str):
		raise TypeError('input must be a string')
	encode = string.encode()
	return hashlib.md5(encode).hexdigest()


def bearer(string) -> str:
	""" base64加密函数 """
	if not isinstance(string, str):
		raise TypeError('input must be a string')
	return base64.b64encode(string.encode()).decode()


@lru_cache(maxsize=None)
def mock():
	""" 生成mock数据 """
	return Mock()


def sqlSelect(sql, key, item=None):
	""" sql查询 """
	return readMysql(sql=sql, key=key, index=int(item) if item else None)


def gen_date_time(step):
	str_date_time = time.strftime('%Y-%m-%d %H_%M_%S').split(' ')
	return str_date_time[int(step)]
