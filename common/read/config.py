from functools import lru_cache

from common.read import SUBJECT_DIR
from utils.read_yaml import read_yaml




@lru_cache(None)  # 缓存
def read_config(filename: str, encoding: str = "utf-8") -> dict:
	""" 读取配置文件 """
	return read_yaml(SUBJECT_DIR.joinpath(filename), encoding)
