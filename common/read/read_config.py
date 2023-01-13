from functools import lru_cache
import yaml
from pathlib import Path


path = Path(__file__).resolve().parent.parent.parent

@lru_cache(None)		# 缓存
def read_config(filename="local.yaml", encoding="utf-8") ->dict:
	""" 读取配置文件 """
	with path.joinpath("config").joinpath(filename).open(encoding=encoding) as f:
		return yaml.load(stream=f, Loader=yaml.FullLoader)
