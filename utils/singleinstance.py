"""
单例模式装饰器
"""
import functools

instances = {}

def singleInstance(cls):
	@functools.wraps(cls)
	def getInstance(*args, **kwargs):
		if not (clsName:= cls.__name__) in instances:
			instances[clsName] = cls(*args,**kwargs)
		return instances[clsName]
	return getInstance