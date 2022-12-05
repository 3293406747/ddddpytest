import yaml
from pathlib import Path
from common.case.render import renderTemplate


path = Path(__file__).resolve().parent.parent.parent
instance = {}

def read_config(filename="local.yaml", encoding="utf-8") ->dict:
	""" 读取配置文件 """
	if not instance.get(filename):
		with path.joinpath("config").joinpath(filename).open(encoding=encoding) as f:
			data = yaml.load(stream=f, Loader=yaml.FullLoader)
		instance[filename] = renderTemplate(data)
	return instance[filename]
