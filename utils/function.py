import base64
import hashlib
import time

from functools import lru_cache

from common.read.mysql import read_mysql
from utils.generate_mock_data.generate_mock_data import GenerateMockData


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
	return GenerateMockData()


def sqlSelect(sql, key, config_path, item=None):
	""" sql查询 """
	return read_mysql(sql=sql, key=key, config_path=config_path, index=int(item) if item else None)


def gen_date_time(step):
	str_date_time = time.strftime('%Y-%m-%d %H_%M_%S').split(' ')
	return str_date_time[int(step)]
