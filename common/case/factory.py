import importlib
import json


class Factory:

	type_ = importlib.import_module("common.case.type_")

	@classmethod
	def create(cls, method, obj, mapping=None):
		Type = getattr(cls.type_, "Type")
		if isinstance(obj, str):
			obj = json.loads(obj)
		if isinstance(obj, list):
			for key, value in enumerate(obj):
				if method == "vary":
					Type.vary(key=key, value=value, mapping=mapping, obj=obj)
				elif method == "func":
					Type.func(key=key, value=value, obj=obj)
				else:
					msg = "method not found"
					raise Exception(msg)
		elif isinstance(obj, dict):
			for key, value in obj.items():
				if method == "vary":
					Type.vary(key=key, value=value, mapping=mapping, obj=obj)
				elif method == "func":
					Type.func(key=key, value=value, obj=obj)
				else:
					msg = "method not found"
					raise Exception(msg)
		return obj



