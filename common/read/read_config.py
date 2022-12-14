import yaml
from pathlib import Path


path = Path(__file__).resolve().parent.parent.parent

def read_config(filename="local.yaml", encoding="utf-8") ->dict:
	""" 读取配置文件 """
	if not read_config.config.get(filename):
		with path.joinpath("config").joinpath(filename).open(encoding=encoding) as f:
			read_config.config[filename] = yaml.load(stream=f, Loader=yaml.FullLoader)
	return read_config.config[filename]

read_config.config = {}
