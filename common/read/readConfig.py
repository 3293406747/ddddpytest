from functools import lru_cache
from pathlib import Path
from utils.yamlReader import yamlReader

CONFIG_DIR = Path(__file__).resolve().parent.parent.parent.joinpath("config")


@lru_cache(None)  # 缓存
def readConfig(filename="local.yaml", encoding="utf-8") -> dict:
	""" 读取配置文件 """
	return yamlReader(CONFIG_DIR.joinpath(filename), encoding)