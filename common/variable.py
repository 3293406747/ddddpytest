import yaml
from pathlib import Path

env_path = Path(__file__).resolve().parent.parent.joinpath("environment")


class Variable:

	def __init__(self):
		self.pool = {}

	def set(self,key,value):
		self.pool[key] = value

	def get(self,key):
		value = self.pool.get(key)
		if value:
			return value
		else:
			raise Exception("未找到该变量")

	def clear(self):
		self.pool.clear()

	@property
	def is_empty(self):
		return self.pool == {}

class Globle(Variable):

	def __init__(self):
		Variable.__init__(self)
		with open(env_path/"globals.yaml",mode="r",encoding="utf-8") as f:
			self.pool = yaml.load(stream=f,Loader=yaml.FullLoader) or {}

class Environment(Variable):

	def __init__(self,env):
		Variable.__init__(self)
		env += ".yaml"
		with open(env_path/env,mode="r",encoding="utf-8") as f:
			self.pool = yaml.load(stream=f,Loader=yaml.FullLoader) or {}

variable = Variable()
global_ = Globle()
environment = Environment("local")
