from functools import lru_cache
from pathlib import Path
from utils.yamlReader import YamlReader

basePath = Path(__file__).resolve().parent.parent.parent

@lru_cache(None)		# 缓存
def readConfig(filename="local.yaml", encoding="utf-8") ->dict:
	""" 读取配置文件 """
	return YamlReader(file=basePath / "config" / filename, encoding=encoding)
