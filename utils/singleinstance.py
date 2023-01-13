instances = {}

def singleInstance(cls):
	def getInstance(*args, **kwargs):
		if not (clsName:= cls.__name__) in instances:
			instances[clsName] = cls(*args,**kwargs)
		return instances[clsName]
	return getInstance