import yaml
from pathlib import Path

path = Path(__file__).resolve()
instance = {}

def read_config():
	""" 读取config """
	if not instance.get("config"):
		with open(file=path.parent.parent / 'config' /'local.yaml', mode="r", encoding="utf-8") as f:
			response = yaml.load(stream=f, Loader=yaml.FullLoader)
		instance['config'] = response
	return instance['config']